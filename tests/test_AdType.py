from src.AdType import AdType, AdTypeId


def test_AdType():
    at1 = AdType(ad_type_id=AdTypeId('0011'),
                 ad_type_name='Chicago Bears',
                 cost_share_rate=0.50,
                 allowed_spend_per_ad=range(200, 201))
    assert(at1.ad_type_id == AdTypeId('0011'))
    assert(at1.ad_type_name == 'Chicago Bears')
    assert(at1.cost_share_rate == .5)
    assert(at1.allowed_spend_per_ad == range(200, 201))
    print(at1)
