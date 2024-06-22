
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
    
    def __init__(self, ads=None):
        '''Purpose, initialize the reimbursement class with an Ads object
        '''
        self.summary_dict = {} # indexed by ad_type: {'<ad_type>': <quantity>}
        self.ads = ads
        self.summarize()

    def summarize(self):
        '''
        maintains a cached data structure of all add types
        '''

    def set_ads(self, ads):
        self.ads = ads
        # reset the summary data structure
        self.summarize()

    def get_ad_types(self):
        return set([ad.ad_type for ad in self.ads])

    def filter_ad_type(self, filter):
        '''
        filter: set, from a subset of valid ad_types
        
        returns new Reimbursement object that has ads from current Reimbursement object
        where the ad_type of the included Ads matches any of the ad types in filter

        '''
        filter = filter.intersection(Ad.VALID_AD_TYPES)
        matched_ads = [ad for ad in self.ads if ad.ad_type in filter]
        return Reimbursement(matched_ads)

    def config(self, config_dict):
        '''
        config_dict has:
            ad_type:
            cost_share_rate:
            allowed_spend_per_ad: (range) - assumption made: this is what is allowed to be reimbursed
        '''

        self.configuration = config_dict

    def compute(self):
        '''
        compute the statistics on the cost share rate and reimbursement amounts per ad_type

        Ad(0011) - cost share rate = .50 and spend per ad is $200(reimbursement amount)
        Ad(0011)
        '''

    def __str__(self):
        return '\n'.join([str(ad) for ad in self.ads])
    


class Ads(list):
    '''
    This is a list of Ad objects
    '''

    def __init__(self):
        super().__init__(self)


class Ad(object):

    VALID_AD_TYPES = set(['0011', '1011', '1111', '1010'])

    def __init__(self, ad_type, ad_name):

        self.ad_type = ad_type
        self.ad_name = ad_name

    def __str__(self):
        return f'Ad_type: {self.ad_type} ... {self.ad_name}'

