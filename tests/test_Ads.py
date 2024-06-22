from src.Ads import Ads, Ad, Reimbursement
from src.AdType import AdTypeId


def test_Ad():

    ad1 = Ad(type=AdTypeId.atid0011, name='Chicago Bears', balance=1_000_000.0)
    ad2 = Ad(type=AdTypeId.atid0011, name='Chicago Fire', balance=450000.0)

    ads = Ads()
    assert(len(ads) == 0)

    ads = Ads([])
    assert(len(ads) == 0)

    ads.append(ad1)
    ads.append(ad2)
    assert(len(ads) == 2)

    ads = Ads([ad1, ad2])
    assert(len(ads) == 2)


def test_Reimbursement():

    ads = Ads([Ad(type=AdTypeId.atid0011, name='Chicago Bears', balance=1_000_000.0),
               Ad(type=AdTypeId.atid0011, name='Chicago Fire', balance=450000.0)])

    reimbursement = Reimbursement(ads)

    reimbursement = Reimbursement(Ads([Ad(type=AdTypeId.atid0011, name='Chicago Bears', balance=1_000_000.0),
                                       Ad(type=AdTypeId.atid0011, name='Chicago Fire', balance=450000.0)]))
    print(reimbursement)
