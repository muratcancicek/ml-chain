from utils.costum_keys import CustomKeys as ck

class WalletStats():
    def __init__(self,account_address : str,**kwargs):
        self.__init__from_dict(**kwargs)
        self.address = account_address
        
    def __init__from_dict(self,**kwargs):
        self.nfts = kwargs[ck.NFTS]
        self.collections = kwargs[ck.COLLECTIONS]
        self.total_transactions = kwargs[ck.TRANSACTIONS][ck.TOTAL]
        self.total_nft_transfer = kwargs[ck.NFT_TRANSFERS][ck.TOTAL]
        self.total_token_transfer = kwargs[ck.TOKEN_TRANSFERS][ck.TOTAL]
        
    def to_dataset_row(self):
        return {
            ck.ADDRESS : self.address,
            ck.NFTS : self.nfts,
            ck.COLLECTIONS : self.collections,
            ck.TOTAL_TRANSACTIONS : self.total_transactions,
            ck.TOTAL_NFT_TRANSFERS : self.total_nft_transfer,
            ck.TOTAL_TOKEN_TRANSFERS : self.total_token_transfer 
        }