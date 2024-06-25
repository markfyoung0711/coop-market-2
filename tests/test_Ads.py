import pytest

from src.Ads import Ads, Ad, Reimbursement


def test_Ad():

    ad1 = Ad(type='0011', name='Chicago Bears', cost=1_000_000.0)
    ad2 = Ad(type='1111', name='Chicago Public Schools', cost=450000.0)

    ads = Ads()
    assert(len(ads) == 0)
    assert(ads.__str__() == '')

    # Task 2: Requirement 1
    ads = Ads([])
    assert(len(ads) == 0)

    ads.append(ad1)
    ads.append(ad2)
    assert(len(ads) == 2)

    assert(ads[0]['type'] == '0011')

    # Task 2: Requirement 4
    assert(ads.__str__() == f"AID: {ad1['aid']}, AdType: 0011, Name: Chicago Bears, Cost: 1000000.00\n"
                            f"AID: {ad2['aid']}, AdType: 1111, Name: Chicago Public Schools, Cost: 450000.00")

    # Task 2: Requirement 1
    ads = Ads([ad1, ad2])
    # Task 2: Requirement 3
    type_counts = ads.get_ad_types()
    assert(type_counts == {'0011': 1, '1111': 1})


def test_Reimbursement():
    '''
        Test Cases: (based on '0011' ad type)

        type  adjusted_cost       minimum     maximum     reimbursement
        0011   100                200          201            0
        0011   200                200          201          200
        0011   201                200          201          200
        1010   500                  0         1000          500
        1010  1400                  0         1000         1000
    '''

    ads = Ads([Ad(type='0011', name='Chicago Bears', cost=200.0),
               Ad(type='0011', name='Chicago Fire', cost=400.0),
               Ad(type='0011', name='Mount Carmel Caravan', cost=402.0),
               Ad(type='1010', name='Miami Dolphins', cost=555.0),
               Ad(type='1010', name='Miami Hurricanes', cost=1555.0),])

    # Test bad construction.
    with pytest.raises(TypeError):
        Reimbursement()

    parameters = [{'ad_type': '0011', 'cost_share_rate': .5, 'minimum_spend_per_ad': 200, 'maximum_spend_per_ad': 201},
                  {'ad_type': '1011', 'cost_share_rate': 1.0, 'minimum_spend_per_ad': 1000, 'maximum_spend_per_ad': 2001},
                  {'ad_type': '1111', 'cost_share_rate': .75, 'minimum_spend_per_ad': 500, 'maximum_spend_per_ad': 501},
                  {'ad_type': '1010', 'cost_share_rate': .90, 'minimum_spend_per_ad': 0, 'maximum_spend_per_ad': 751},]

    # Test getting ads, ad_types,
    reimbursement = Reimbursement(parameters=parameters, ads=ads)
    assert(reimbursement.get_ads() == ads)
    assert(reimbursement.get_ad_types() == set(['0011', '1010']))

    # Test reimbursement amounts per Ad, and total of all Ads
    results = reimbursement.compute()
    # Bears: they did not spend enough, minimum was 200
    assert(results.loc[results['name'] == 'Chicago Bears', 'reimbursement'].values[0] == 0)
    # Fire: spent exactly the minimum
    assert(results.loc[results['name'] == 'Chicago Fire', 'reimbursement'].values[0] == 200)
    # Caravan: spent over maximum
    assert(results.loc[results['name'] == 'Mount Carmel Caravan', 'reimbursement'].values[0] == 200)
    # Dolphins: should get 499.5 back
    assert(results.loc[results['name'] == 'Miami Dolphins', 'reimbursement'].values[0] == 499.5)
    # Hurricanes: should get 750 back
    assert(results.loc[results['name'] == 'Miami Hurricanes', 'reimbursement'].values[0] == 750)

    # Task 2: Requirement 5
    reimbursement_total = reimbursement.compute_reimbursement_total(results)
    assert(reimbursement_total == 1649.5)

    '''
    Sample of merged results
                                    aid  type                  name    cost ad_type  cost_share_rate  minimum_spend_per_ad  maximum_spend_per_ad  adjusted_cost  reimbursement
0  21049f78-f2f7-4849-9b22-902e663e6c32  0011         Chicago Bears   200.0    0011              0.5                   200                   201          100.0            0.0
1  7b7be20f-3ccf-47bd-8150-7bbcfba83d1f  0011          Chicago Fire   400.0    0011              0.5                   200                   201          200.0          200.0
2  11541fef-728d-4633-b74e-d316d01ef516  0011  Mount Carmel Caravan   402.0    0011              0.5                   200                   201          201.0          200.0
3  9f811d66-6ddc-4e2f-92a0-96373a8cd5d4  1010        Miami Dolphins   555.0    1010              0.9                     0                   751          499.5          499.5
4  5aa1e6ac-2a34-471c-80e0-ec6dcdf4bf48  1010      Miami Hurricanes  1555.0    1010              0.9                     0                   751         1399.5          750.0
    '''

    print(f'\n{reimbursement}')

    # Task 2: Requirement 3
    reimb2 = reimbursement.filter_ad_type(set(['0011']))
    results = reimb2.compute()
    total = reimb2.compute_reimbursement_total(results)
    assert(total == 400)
