from moralis import evm_api
import json
from utils.costum_keys import CustomKeys as ck

class QueryHandler:
    def __init__(self, path_prefix = ''):
        self.__path_prefix = path_prefix
        self.__api_keys =  self.__read_api_key()

    def __read_api_key(self):
        with open(self.__path_prefix + 'data/api_keys.json', 'r') as file:
            self.__api_keys = json.loads(file.read())
        return self.__api_keys
    
    def get_wallet_data(self, wallet_address):
        result = evm_api.wallets.get_wallet_active_chains(
            api_key=self.__api_keys[ck.MORALIS],
            params={ 'address': wallet_address },
        )
        return result
    
    def get_wallet_transactions(self, address, chain = 'eth', order = 'DESC'):
        params = { 'chain': chain, 'order': order,  'address': address }
        transactions = []
        while ck.CURSOR not in params or params[ck.CURSOR]:
            page = evm_api.transaction.get_wallet_transactions(
                api_key=self.__api_keys[ck.MORALIS], 
                params=params,
            )
            transactions.extend(page[ck.RESULT])
            params[ck.CURSOR] = page[ck.CURSOR]
            break
        return transactions
    
    def get_wallet_stats(self, address, chain = "eth"):
        params = { 'chain': chain, 'address': address}
        result = evm_api.wallets.get_wallet_stats(
            api_key = self.__api_keys[ck.MORALIS],
            params = params
        )
        return result