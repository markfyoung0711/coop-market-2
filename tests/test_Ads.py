from src.Ads import Ads, Ad, Reimbursement


def test_Ad():

    RAW_DATA = [('1001', 'Mark Ad 1'), ('1002', 'Sean Ad 1'), ('1003', 'Donna Ad 1')]
    ads = Ads()
    for ad_type, ad_name in RAW_DATA:
        ads.append(Ad(ad_type, ad_name))

    r1 = Reimbursement(ads)
    print(r1)
    breakpoint()
        

    


