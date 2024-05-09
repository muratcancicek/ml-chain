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

    def read_wallet_stats_for_last_512(self):
        return pd.read_csv(self.__path_prefix + 'data/wallet_stats_for_last_512.csv')

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

    def query_time_to_dataset_row(self,address,total_trs,query_time):
        return {
            ck.ADDRESS : address,
            ck.TOTAL_TRANSACTIONS : total_trs,
            ck.QUERY_TIME : query_time
        }
        
    def save_dataset_from_addresses(self, addresses, flags, save_time_table = True,label_sources=[], total_transactions = []):
        accounts = []
        times = []
        total_addresses = len(addresses)
        if not label_sources:
            label_sources = [ck.MORALIS for _ in range(total_addresses)]
        if not total_transactions:
            total_transactions = [0 for _ in range(total_addresses)]
        for i, (a, f, src, trs) in enumerate(zip(addresses, flags, label_sources,total_transactions)):
            try:
                start_time = datetime.now()
                account = self.query_account(a, f, src).to_dataset_row()
                end_time = datetime.now()
                accounts.append(account)
                
                query_time = str(end_time-start_time)
                query_dataset_row = self.query_time_to_dataset_row(a,trs,query_time)
                times.append(query_dataset_row)
                
                progress = f'{((i+1)/total_addresses)*100:.2f}'
                print(f"\rProcessing: {progress}%", end="")
            except Exception as e:
                print(f"\nError processing address: {a}")
                print(e)
                self.save_error_address(a)
                continue
        dataset = pd.DataFrame(accounts)
        self.save_dataset(dataset,"data/mev_bots/dataset")
        
        if save_time_table:
            time_dataset = pd.DataFrame(times)
            self.save_dataset(time_dataset,"data/mev_bots/minutes")
        return

    def save_updated_dataset(self, base_dataset):
        addresses = base_dataset[ck.ADDRESS].tolist()
        flags = base_dataset[ck.FLAG].tolist()
        self.save_dataset_from_addresses(addresses, flags)
        return

    def save_mev_bots_in_base_dataset(self,min_transaction = 0,max_transaction = 0):
        base_dataset = self.read_base_dataset()
        base_dataset = base_dataset[
            (base_dataset[ck.FLAG] == ck.MEV_BOT_FLAG) |
            (base_dataset[ck.FLAG] == ck.SPAM_FLAG)
            ]
        wallet_stats = self.read_wallet_stats_for_last_512()
        
        length = len(wallet_stats)
        addresses = []
        flags = []
        total_transactions = []
        
        for i in range(length):
            total_transaction = wallet_stats[ck.TOTAL_TRANSACTIONS][i]
            if min_transaction < total_transaction < max_transaction:
                address = wallet_stats[ck.ADDRESS][i]
                base_data = base_dataset[(base_dataset[ck.ADDRESS] == address)].iloc[0]
                addresses.append(address)
                flags.append(base_data[ck.FLAG])
                total_transactions.append(total_transaction)
        self.save_dataset_from_addresses(addresses,flags,total_transactions= total_transactions)
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
                print(f"\rProceed in {i+1}/{total_address}",end="")
            except Exception as e:
                print(f"\nError {e} processing in address {address}")
                self.save_error_address(address)
                continue
        dataset = pd.DataFrame(all_stats)
        self.save_dataset(dataset,"data/stats")
        return
    
    def save_stats_for_base_dataset(self,start_ind = 0,end_ind = None):
        base_dataset = self.read_base_dataset()
        base_addresses = base_dataset.iloc[start_ind:end_ind][ck.ADDRESS].to_list()
        self.save_stats_from_addresses(base_addresses)
        
    def save_dataset(self,dataset: pd.DataFrame, save_address: str):
        now_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        prefix = self.__path_prefix
        dataset.to_csv(f'{prefix}{save_address}_{now_str}.csv', index=False)
        print("\nDataset saved successfully.")
        
    def save_error_address(self,address):
        with open("data/mev_bots/error_addresses.txt","w") as error_addresses:
            error_addresses.write(f"\n{address}")