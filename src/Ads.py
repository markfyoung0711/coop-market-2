from uuid import uuid4

import pandas as pd


class Reimbursement(object):
    '''Reimbursement is used to compute ads of different types,
       the total amount of reimbursement for them,
       and other Reimbursement classes made up of subsets of different ad types

    Class Methods:

        - initialize : to create itself with an associated Ads object

        - set_ads : to replace the associated Ads object

        - get_ad_type : to query all possible ad types

        - filter_ad_type : to build a new Reimbursement object for arbitrary set of add types

        - configure : to set up new valid ad types and their parameters,
            cost_share_rate
            allowed_spend_per_ad_range_dollars
            - this is a range object.  for a fixed number, range would be range(200,201) (for $200)

    __str__ to print the Ads object associated with the add
    '''

    def __init__(self, parameters, ads):
        '''
        Purpose, initialize the reimbursement class with an Ads object

        Parameters:
        -----------
        parameters: dict, reimbursement parameters for each ad type covered by this Reimbursement object
                  at a minimum, parameters must include these dict keys:
                    'ad_type',
                    'cost_share_rate', (float)
                    'minimum_spend_per_ad', (float)
                    'maximum_spend_per_ad' (float)

        ads: list, of Ad objects, if empty, it is expected to be attached later
        '''

        self.summary_dict = {}
        self.parameters = pd.DataFrame(parameters)
        for col in ['cost_share_rate', 'minimum_spend_per_ad', 'maximum_spend_per_ad']:
            self.parameters[col] = self.parameters[col].astype(float)
        self.ads = ads

    def compute_reimbursement_total(self, reimbursements_per_ad):
        return reimbursements_per_ad['reimbursement'].sum()

    def compute(self):
        '''Compute reimbursement:

        'cost' = cost of add
        'cost_share_rate' = rate to compute shareable cost
        'min' = minimum of reimbursement
        'max' = maximum amount of reimbursement

        'adjusted_cost' = 'cost' * 'cost_share_rate'

             aid  type           name    balance ad_type  cost_share_rate  minimum_spend_per_ad  maximum_spend_per_ad
        0  19230  0011  Chicago Bears  1000000.0    0011              0.5                   200                   201
        1  92929  0011   Chicago Fire   450000.0    0011              0.5                   200                   201

        Test Cases:
        adjusted_cost       minimum     maximum     reimbursement
        100                 200         201            0
        200                 200         201          200
        201                 200         201          200
        500                 0          1000          500
        1500                0          1000         1000

        if min - adjusted_cost > 0: reimbursement = 0
        elif max - adjusted_cost > 0: reimbursement = adjusted_cost
        else: reimbursement = max - 1

        1. compute adjusted_cost
        2. define lambda
        3. apply lambda
        '''

        # merge the Ads and the Reimbursement parameters on ad_type
        results = pd.merge(pd.DataFrame(self.ads), self.parameters, left_on=['type'], right_on=['ad_type'], how='left')
        results['adjusted_cost'] = results['cost'].astype(float) * results['cost_share_rate']

        # compute the reimbursement.  Leave zero reimbursement until last to simplify
        reimb_idx = results['adjusted_cost'] >= results['minimum_spend_per_ad']
        results.loc[reimb_idx, 'reimbursement'] = \
            results.loc[reimb_idx].apply(lambda rec: min(rec['adjusted_cost'], rec['maximum_spend_per_ad'] - 1), axis='columns')
        # zero reimbursement as it didn't achieve the minimum ad spend
        no_reimb_idx = results['adjusted_cost'] < results['minimum_spend_per_ad']
        results.loc[no_reimb_idx, 'reimbursement'] = 0.0

        return results

    def set_ads(self, ads):
        self.ads = ads

    def get_ads(self):
        return self.ads

    def get_ad_types(self):
        return set([ad['type'] for ad in self.ads])

    def filter_ad_type(self, filter_set):
        '''
        filter_set: set, from a subset of valid ad_types

        returns new Reimbursement object that has ads from current Reimbursement object
        where the ad_type of the included Ads matches any of the ad types in filter

        '''
        filter_set = filter_set.intersection(set(self.parameters['ad_type']))
        matched_ads = [ad for ad in self.ads if ad['type'] in filter_set]
        return Reimbursement(self.parameters, matched_ads)

    def __str__(self):
        return '\n'.join([str(ad) for ad in self.ads])


class Ads(list):
    '''
    This is a list of Ad objects
    '''

    dataframe = None

    def __init__(self, ad_list=[]):
        '''
        ad_list: list of Ad objects
        '''
        super().__init__(ad_list)
        self.set_ad_types()

    def set_ad_types(self):
        if len(self) > 0:
            self.types = pd.DataFrame(self)['type'].value_counts().to_dict()
        else:
            self.types = None

    def __str__(self):
        return '\n'.join([str(ad) for ad in self])

    def get_ad_types(self):
        self.set_ad_types()
        return self.types


class Ad(dict):
    '''
    aid: uuid4, the unique identifier for the ad - not sure if this is a thing, but would think so
    type: AddType, the ad type
    name: str, the name of the ad
    cost: float, the total cost of Ad
    '''

    def __init__(self, type, name, cost=0):
        self['aid'] = uuid4()
        self['type'] = type
        self['name'] = name
        self['cost'] = cost

    def __str__(self):
        return ', '.join([f'AID: {self["aid"]}',
                          f'AdType: {self["type"]}',
                          f'Name: {self["name"]}',
                          f'Cost: {self["cost"]:.2f}'])
