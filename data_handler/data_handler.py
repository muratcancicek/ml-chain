import pandas as pd
from datetime import datetime
import json

from data_handler.query_handler import QueryHandler
from utils.costum_keys import CustomKeys as ck
from models.transaction import Transaction
from models.account import Account
from models.stats import WalletStats

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
        dataset = pd.DataFrame(accounts)
        self.save_dataset(dataset,"dataset")
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
        length = len(base_dataset)
        i = 0
        subset_size = 50
        while i < length:
            subset = base_dataset[i:i+subset_size]
            addresses = subset[ck.ADDRESS].tolist()
            flags = subset[ck.FLAG].tolist()
            self.save_dataset_from_addresses(addresses, flags)
            i += subset_size
        return

    def query_stats(self,address):
        stats = self.__query_handler.get_wallet_stats(address)
        return WalletStats(address,**stats)

    def save_stats_from_addresses(self,addresses):
        all_stats = []
        total_address = len(addresses)
        for i in range(total_address):
            address = addresses[i]
            try:
                wallet_stat = self.query_stats(address).to_dataset_row()
                all_stats.append(wallet_stat)
                print(f"Proceed in {i+1}/{total_address}")
            except Exception as e:
                print(f"\nError {e} processing in address {address}")
                continue
        dataset = pd.DataFrame(all_stats)
        self.save_dataset(dataset,"stats")
        return
    
    def save_stats_for_base_dataset(self,start_ind = 0,end_ind = None):
        base_dataset = self.read_base_dataset()
        base_addresses = base_dataset.iloc[start_ind:end_ind][ck.ADDRESS].to_list()
        self.save_stats_from_addresses(base_addresses)
        
    def save_dataset(self,dataset: pd.DataFrame, dataset_name: str):
        now_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        prefix = self.__path_prefix
        dataset.to_csv(f'{prefix}data/{dataset_name}_{now_str}.csv', index=False)
        print("\nWallet stats saved successfully.")