from dune_client.client import DuneClient
from dune_client.query import QueryBase
from dune_client.types import QueryParameter

import pandas as pd
import time
import json

from utils.costum_keys import CustomKeys as ck

class DuneHandler():
    def __init__(self,file_name,path_prefix = ""):
        self.__path_prefix = path_prefix
        self.__file_name = file_name
        self.__query_id = 3894747
        self.__path = path_prefix + "data/" + file_name + ".csv"
        self.__api_keys = self.__read_api_keys()
        self.__dune_client = DuneClient(
            api_key = self.__api_keys[ck.DUNE],
            base_url = "https://api.dune.com",
            request_timeout = 300    
        )
    def __read_api_keys(self):
        with open(self.__path_prefix + "data/api_keys.json") as file:
            self.__api_keys = json.loads(file.read())
        return self.__api_keys
    
    def get_base_addresses(self):
        return list(pd.read_csv(self.__path)["wallet_address"])
    
    def get_arranged_address_list_for_query(self,addresses,count_limit = 1000):
        address_list = ["("]
        
        for i in range(len(addresses) + 1):
            added_index = i//count_limit
            
            if (i == len(addresses)):
                address_list[added_index] = address_list[added_index][:-1]
                address_list[added_index] += ")"
                break
            
            elif i % count_limit == 0 and i != 0:
                address_list[added_index - 1] = address_list[added_index - 1][:-1]
                address_list[added_index - 1] += ")"
                address_list.append("(")
            
            address_list[added_index] += f"{addresses[i]},"
        return address_list 

    def create_query(self,address):
        return QueryBase(
            query_id=self.__query_id,
            params=[QueryParameter.text_type(name="address", value=address)],
        )
        
    def get_transaction(self,query):
        return self.__dune_client.run_query_dataframe(query=query)

    def get_all_transactions(self,addresses):
        all_transactions = pd.DataFrame(columns=["block_time","value","from","to"])
        
        for i in range(len(addresses)):
            print(f"***********{i+1}/{len(addresses)} query**********")
            query = self.create_query(addresses[i])
            while True:
                try:
                    transactions = self.get_transaction(query)
                    break
                except Exception:
                    time.sleep(5)
            all_transactions = pd.concat([all_transactions,transactions],ignore_index=True)
            
        return all_transactions

    def save_transactions(self,transactions,save_path):
        transactions.to_csv(save_path)

    def count_unique_address(self,address_list):
        return len(set(address_list))

    def get_base_transactions_from_csv(self):
        csv_path = self.__path_prefix + f"data/{self.__file_name}_transactions.csv"
        return pd.read_csv(csv_path)

    def count_total_unique_transactions(self):
        from_addresses = self.get_base_transactions_from_csv()["from"]
        to_addresses = self.get_base_transactions_from_csv()["to"]

        unique_from_address_count = self.count_unique_address(from_addresses)
        unique_to_address_count = self.count_unique_address(to_addresses)

        print(f"Total Transactions Count: {len(from_addresses)}")
        print(f"Unique from Address Count: {unique_from_address_count}")
        print(f"Unique to Address Count: {unique_to_address_count}")

    def save_base_transactions(self):
        addresses = self.get_base_addresses()[:10]
        arranged_addresses = self.get_arranged_address_list_for_query(addresses)
        base_transactions = self.get_all_transactions(arranged_addresses)
        
        save_path = self.__path_prefix + f"data/{self.__file_name}_transactions_first10.csv"
        self.save_transactions(base_transactions,save_path)
        
    
    def save_parent_transactions(self,level_limit):
        transactions = self.get_base_transactions_from_csv().head(10)
        for i in range(level_limit):
            addresses = list(set(transactions["from"]))
            arranged_addresses = self.get_arranged_address_list_for_query(addresses)
            transactions = self.get_all_transactions(arranged_addresses)
            
            save_path = self.__path_prefix + f"data/{self.__file_name}_transactions_parent{i+1}.csv"
            self.save_transactions(transactions,save_path)
    
    def save_child_transactions(self,level_limit):
        transactions = self.get_base_transactions_from_csv().head(10)
        for i in range(level_limit):
            addresses = list(set(transactions["to"]))
            arranged_addresses = self.get_arranged_address_list_for_query(addresses)
            transactions = self.get_all_transactions(arranged_addresses)
            
            save_path = self.__path_prefix + f"data/{self.__file_name}_transactions_child{i+1}.csv"
            self.save_transactions(transactions,save_path)

dune_handler = DuneHandler("airdrop1_claims")
dune_handler.save_base_transactions()
# dune_handler.save_parent_transactions(5)
# dune_handler.save_child_transactions(5)
