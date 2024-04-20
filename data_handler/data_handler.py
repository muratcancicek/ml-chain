import pandas as pd
from datetime import datetime
import json

from data_handler.query_handler import QueryHandler
from utils.costum_keys import CustomKeys as ck
from models.transaction import Transaction
from models.account import Account

class DataHandler(object):
    def __init__(self, path_prefix = ''):
        self.__path_prefix = path_prefix
        self.__query_handler = QueryHandler(path_prefix)
        self.__read_erc20_signatures()

    def __read_erc20_signatures(self):
        prefix = self.__path_prefix
        erc20_signatures_path = prefix + f'data/ERC20_signatures.json'
        erc20_signatures_file = open(erc20_signatures_path, 'r')
        self.__erc20_signatures = json.loads(erc20_signatures_file.read())
        return

    def read_base_dataset(self):
        return pd.read_csv(self.__path_prefix + 'data/uxly_dataset.csv')

    def query_wallet_data(self, wallet_address):
        return self.__query_handler.get_wallet_data(wallet_address)

    def __add_erc20_signature(self, tnx_dict):
        signs = self.__erc20_signatures
        tnx_dict[ck.ERC20_CODE] = tnx_dict[ck.INPUT][:10] 
        tnx_dict[ck.IS_ERC20] = tnx_dict[ck.ERC20_CODE] in signs
        tnx_dict[ck.ERC20_FUNCTION] = signs.get(tnx_dict[ck.ERC20_CODE], None)
        return tnx_dict    

    def query_wallet_transactions(self, address, chain='eth', order='DESC'):
        t = self.__query_handler.get_wallet_transactions(address, chain, order)
        transactions = [self.__add_erc20_signature(tnx) for tnx in t]
        transactions = [Transaction(address, **tnx) for tnx in transactions]
        return transactions

    def query_account(self, address, flag: int, label_source: str = ''):
        if not label_source:
            label_source = ck.ETHERSCAN
        transactions = self.query_wallet_transactions(address)
        return Account(
            address=address, 
            transactions=transactions, 
            flag=flag, 
            label_source=label_source,
            data_source=ck.MORALIS,
            )

    def save_dataset_from_addresses(self, addresses, flags, label_sources=[]):
        accounts = []
        total_addresses = len(addresses)
        if not label_sources:
            label_sources = [ck.MORALIS for _ in range(total_addresses)]
        for i, (a, f, src) in enumerate(zip(addresses, flags, label_sources)):
            try:
                account = self.query_account(a, f, src).to_dataset_row()
                accounts.append(account)
                progress = f'{((i+1)/total_addresses)*100:.2f}'
                print(f"\rProcessing: {progress}%", end="")
            except Exception as e:
                print(f"\nError processing address: {a}")
                print(e)
                continue
        now_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        dataset = pd.DataFrame(accounts)
        prefix = self.__path_prefix
        dataset.to_csv(f'{prefix}data/dataset_{now_str}.csv', index=False)
        print("\nDataset saved successfully.")
        return

    def save_updated_dataset(self, base_dataset):
        addresses = base_dataset[ck.ADDRESS].tolist()
        flags = base_dataset[ck.FLAG].tolist()
        self.save_dataset_from_addresses(addresses, flags)
        return

    def save_mev_bots_in_base_dataset(self):
        base_dataset = self.read_base_dataset()
        base_dataset = base_dataset[
            (base_dataset[ck.FLAG] == ck.MEV_BOT_FLAG) |
            (base_dataset[ck.FLAG] == ck.SPAM_FLAG)
            ]
        self.save_updated_dataset(base_dataset)
        return