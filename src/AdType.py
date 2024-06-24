class AdType(object):

    def __init__(self, ad_type_id, ad_type_name, cost_share_rate, allowed_spend_per_ad):
        self.ad_type_id = ad_type_id
        self.ad_type_name = ad_type_name if ad_type_name else f'AdType for {self.ad_type_id}'
        self.cost_share_rate = cost_share_rate
        self.allowed_spend_per_ad = allowed_spend_per_ad

    def __str__(self):
        return '\n'.join([f'AdTypeName {self.ad_type_name}',
                          f'AdTypeId: {self.ad_type_id}',
                          f'CostShareRate: {self.cost_share_rate}',
                          f'Allowed Spend Per Ad: {self.allowed_spend_per_ad}'])
