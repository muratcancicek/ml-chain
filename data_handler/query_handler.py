from moralis import evm_api

class QueryHandler:
    def __init__(self):
        self.__api_key =  self.__read_api_key()

    def __read_api_key(self):
        with open('../data/api_key.txt', 'r') as file:
            self.__api_key = file.read().replace('\n', '')
        return self.__api_key
    
    def get_wallet_data(self, wallet_address):
        result = evm_api.wallets.get_wallet_active_chains(
            api_key=self.__api_key,
            params={ "address": wallet_address },
        )
        return result