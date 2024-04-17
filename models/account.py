from data_handler.transaction_history_handler import TransactionHistoryHandler
from utils.costum_keys import DatasetOneKeys as dk, CustomKeys as ck

class Account(object): 
    def __init__(self, from_dataset: bool = False, **kwargs):
        if from_dataset:
            self.__init__from_dataset(**kwargs)
        else:
            self.__init__from_history(**kwargs)

    def __init__from_dataset(self, **kwargs):
        self.__fields = { **kwargs }
        self.address = kwargs[dk.address]
        self.FLAG = kwargs[dk.FLAG]
        self.avg_min_between_sent_tnx = kwargs[dk.avg_min_between_sent_tnx]
        self.avg_min_between_received_tnx = kwargs[dk.avg_min_between_received_tnx]
        self.time_diff_between_first_and_last_mins = kwargs[dk.time_diff_between_first_and_last_mins]
        self.sent_tnx = kwargs[dk.sent_tnx]
        self.received_tnx = kwargs[dk.received_tnx]
        self.number_of_created_contracts = kwargs[dk.number_of_created_contracts]
        self.unique_received_from_addresses = kwargs[dk.unique_received_from_addresses]
        self.unique_sent_to_addresses = kwargs[dk.unique_sent_to_addresses]
        self.min_value_received = kwargs[dk.min_value_received]
        self.max_value_received = kwargs[dk.max_value_received]
        self.avg_val_received = kwargs[dk.avg_val_received]
        self.min_val_sent = kwargs[dk.min_val_sent]
        self.max_val_sent = kwargs[dk.max_val_sent]
        self.avg_val_sent = kwargs[dk.avg_val_sent]
        self.min_value_sent_to_contract = kwargs[dk.min_value_sent_to_contract]
        self.max_val_sent_to_contract = kwargs[dk.max_val_sent_to_contract]
        self.avg_value_sent_to_contract = kwargs[dk.avg_value_sent_to_contract]
        self.total_transactions_including_tnx_to_create_contract = kwargs[dk.total_transactions_including_tnx_to_create_contract]
        self.total_ether_sent = kwargs[dk.total_ether_sent]
        self.total_ether_received = kwargs[dk.total_ether_received]
        self.total_ether_sent_contracts = kwargs[dk.total_ether_sent_contracts]
        self.total_ether_balance = kwargs[dk.total_ether_balance]
        self.total_ERC20_tnxs = kwargs[dk.total_ERC20_tnxs]
        self.ERC20_total_ether_received = kwargs[dk.ERC20_total_ether_received]
        self.ERC20_total_ether_sent = kwargs[dk.ERC20_total_ether_sent]
        self.ERC20_total_ether_sent_contract = kwargs[dk.ERC20_total_ether_sent_contract]
        self.ERC20_uniq_sent_addr = kwargs[dk.ERC20_uniq_sent_addr]
        self.ERC20_uniq_rec_addr = kwargs[dk.ERC20_uniq_rec_addr]
        self.ERC20_uniq_sent_addr_1 = kwargs[dk.ERC20_uniq_sent_addr_1]
        self.ERC20_uniq_rec_contract_addr = kwargs[dk.ERC20_uniq_rec_contract_addr]
        self.ERC20_avg_time_between_sent_tnx = kwargs[dk.ERC20_avg_time_between_sent_tnx]
        self.ERC20_avg_time_between_rec_tnx = kwargs[dk.ERC20_avg_time_between_rec_tnx]
        self.ERC20_avg_time_between_rec_2_tnx = kwargs[dk.ERC20_avg_time_between_rec_2_tnx]
        self.ERC20_avg_time_between_contract_tnx = kwargs[dk.ERC20_avg_time_between_contract_tnx]
        self.ERC20_min_val_rec = kwargs[dk.ERC20_min_val_rec]
        self.ERC20_max_val_rec = kwargs[dk.ERC20_max_val_rec]
        self.ERC20_avg_val_rec = kwargs[dk.ERC20_avg_val_rec]
        self.ERC20_min_val_sent = kwargs[dk.ERC20_min_val_sent]
        self.ERC20_max_val_sent = kwargs[dk.ERC20_max_val_sent]
        self.ERC20_avg_val_sent = kwargs[dk.ERC20_avg_val_sent]
        self.ERC20_min_val_sent_contract = kwargs[dk.ERC20_min_val_sent_contract]
        self.ERC20_max_val_sent_contract = kwargs[dk.ERC20_max_val_sent_contract]
        self.ERC20_avg_val_sent_contract = kwargs[dk.ERC20_avg_val_sent_contract]
        self.ERC20_uniq_sent_token_name = kwargs[dk.ERC20_uniq_sent_token_name]
        self.ERC20_uniq_rec_token_name = kwargs[dk.ERC20_uniq_rec_token_name]
        self.ERC20_most_sent_token_type = kwargs[dk.ERC20_most_sent_token_type]
        self.ERC20_most_rec_token_type = kwargs[dk.ERC20_most_rec_token_type]
        self.source = kwargs[dk.source]
        return

    def __init__from_history(self, **kwargs):
        self.__fields = { **kwargs }
        self.address = kwargs[ck.ADDRESS]
        self.FLAG = kwargs[ck.FLAG]
        self.source = kwargs[ck.SOURCE]
        handler = TransactionHistoryHandler(kwargs[ck.TRANSACTIONS])
        self.avg_min_between_sent_tnx = \
            handler.calculate_avg_min_between_sent_tnx()
        self.avg_min_between_received_tnx = \
            handler.calculate_avg_min_between_received_tnx()
        self.time_diff_between_first_and_last_mins = \
            handler.calculate_time_diff_between_first_and_last_mins()
        self.sent_tnx = handler.calculate_sent_tnx()
        self.received_tnx = handler.calculate_received_tnx()
        self.number_of_created_contracts = \
            handler.calculate_number_of_created_contracts()
        self.unique_received_from_addresses = \
            handler.calculate_unique_received_from_addresses()
        self.unique_sent_to_addresses = \
            handler.calculate_unique_sent_to_addresses()
        self.min_value_received = handler.calculate_min_value_received()
        self.max_value_received = handler.calculate_max_value_received()
        self.avg_val_received = handler.calculate_avg_val_received()
        self.min_val_sent = handler.calculate_min_val_sent()
        self.max_val_sent = handler.calculate_max_val_sent()
        self.avg_val_sent = handler.calculate_avg_val_sent()
        self.min_value_sent_to_contract = \
            handler.calculate_min_value_sent_to_contract()
        self.max_val_sent_to_contract = \
            handler.calculate_max_val_sent_to_contract()
        self.avg_value_sent_to_contract = \
            handler.calculate_avg_value_sent_to_contract()
        self.total_transactions_including_tnx_to_create_contract = \
            handler.calculate_total_transactions_including_tnx_to_create_contract()
        self.total_ether_sent = handler.calculate_total_ether_sent()
        self.total_ether_received = handler.calculate_total_ether_received()
        self.total_ether_sent_contracts = \
            handler.calculate_total_ether_sent_contracts()
        self.total_ether_balance = handler.calculate_total_ether_balance()
        self.total_ERC20_tnxs = handler.calculate_total_ERC20_tnxs()
        self.ERC20_total_ether_received = \
            handler.calculate_ERC20_total_ether_received()
        self.ERC20_total_ether_sent = \
            handler.calculate_ERC20_total_ether_sent()
        self.ERC20_total_ether_sent_contract = \
            handler.calculate_ERC20_total_ether_sent_contract()
        self.ERC20_uniq_sent_addr = handler.calculate_ERC20_uniq_sent_addr()
        self.ERC20_uniq_rec_addr = handler.calculate_ERC20_uniq_rec_addr()
        self.ERC20_uniq_sent_addr_1 = \
            handler.calculate_ERC20_uniq_sent_addr_1()
        self.ERC20_uniq_rec_contract_addr = \
            handler.calculate_ERC20_uniq_rec_contract_addr()
        self.ERC20_avg_time_between_sent_tnx = \
            handler.calculate_ERC20_avg_time_between_sent_tnx()
        self.ERC20_avg_time_between_rec_tnx = \
            handler.calculate_ERC20_avg_time_between_rec_tnx()
        self.ERC20_avg_time_between_rec_2_tnx = \
            handler.calculate_ERC20_avg_time_between_rec_2_tnx()
        self.ERC20_avg_time_between_contract_tnx = \
            handler.calculate_ERC20_avg_time_between_contract_tnx()
        self.ERC20_min_val_rec = handler.calculate_ERC20_min_val_rec()
        self.ERC20_max_val_rec = handler.calculate_ERC20_max_val_rec()
        self.ERC20_avg_val_rec = handler.calculate_ERC20_avg_val_rec()
        self.ERC20_min_val_sent = handler.calculate_ERC20_min_val_sent()
        self.ERC20_max_val_sent = handler.calculate_ERC20_max_val_sent()
        self.ERC20_avg_val_sent = handler.calculate_ERC20_avg_val_sent()
        self.ERC20_min_val_sent_contract = \
            handler.calculate_ERC20_min_val_sent_contract()
        self.ERC20_max_val_sent_contract = \
            handler.calculate_ERC20_max_val_sent_contract()
        self.ERC20_avg_val_sent_contract = \
            handler.calculate_ERC20_avg_val_sent_contract()
        self.ERC20_uniq_sent_token_name = \
            handler.calculate_ERC20_uniq_sent_token_name()
        self.ERC20_uniq_rec_token_name = \
            handler.calculate_ERC20_uniq_rec_token_name()
        self.ERC20_most_sent_token_type = \
            handler.calculate_ERC20_most_sent_token_type()
        self.ERC20_most_rec_token_type = \
            handler.calculate_ERC20_most_rec_token_type()

        return

    def __getitem__(self, key):
        try:
            return self.__fields[key]
        except KeyError:
            raise KeyError(f"The key '{key}' was not found in the metadata.")

    def to_dataset_row(self):
        return {
            dk.address: self.address,
            dk.FLAG: self.FLAG,
            dk.avg_min_between_sent_tnx: self.avg_min_between_sent_tnx,
            dk.avg_min_between_received_tnx: self.avg_min_between_received_tnx,
            dk.time_diff_between_first_and_last_mins: self.time_diff_between_first_and_last_mins,
            dk.sent_tnx: self.sent_tnx,
            dk.received_tnx: self.received_tnx,
            dk.number_of_created_contracts: self.number_of_created_contracts,
            dk.unique_received_from_addresses: self.unique_received_from_addresses,
            dk.unique_sent_to_addresses: self.unique_sent_to_addresses,
            dk.min_value_received: self.min_value_received,
            dk.max_value_received: self.max_value_received,
            dk.avg_val_received: self.avg_val_received,
            dk.min_val_sent: self.min_val_sent,
            dk.max_val_sent: self.max_val_sent,
            dk.avg_val_sent: self.avg_val_sent,
            dk.min_value_sent_to_contract: self.min_value_sent_to_contract,
            dk.max_val_sent_to_contract: self.max_val_sent_to_contract,
            dk.avg_value_sent_to_contract: self.avg_value_sent_to_contract,
            dk.total_transactions_including_tnx_to_create_contract: self.total_transactions_including_tnx_to_create_contract,
            dk.total_ether_sent: self.total_ether_sent,
            dk.total_ether_received: self.total_ether_received,
            dk.total_ether_sent_contracts: self.total_ether_sent_contracts,
            dk.total_ether_balance: self.total_ether_balance,
            dk.total_ERC20_tnxs: self.total_ERC20_tnxs,
            dk.ERC20_total_ether_received: self.ERC20_total_ether_received,
            dk.ERC20_total_ether_sent: self.ERC20_total_ether_sent,
            dk.ERC20_total_ether_sent_contract: self.ERC20_total_ether_sent_contract,
            dk.ERC20_uniq_sent_addr: self.ERC20_uniq_sent_addr,
            dk.ERC20_uniq_rec_addr: self.ERC20_uniq_rec_addr,
            dk.ERC20_uniq_sent_addr_1: self.ERC20_uniq_sent_addr_1,
            dk.ERC20_uniq_rec_contract_addr: self.ERC20_uniq_rec_contract_addr,
            dk.ERC20_avg_time_between_sent_tnx: self.ERC20_avg_time_between_sent_tnx,
            dk.ERC20_avg_time_between_rec_tnx: self.ERC20_avg_time_between_rec_tnx,
            dk.ERC20_avg_time_between_rec_2_tnx: self.ERC20_avg_time_between_rec_2_tnx,
            dk.ERC20_avg_time_between_contract_tnx: self.ERC20_avg_time_between_contract_tnx,
            dk.ERC20_min_val_rec: self.ERC20_min_val_rec,
            dk.ERC20_max_val_rec: self.ERC20_max_val_rec,
            dk.ERC20_avg_val_rec: self.ERC20_avg_val_rec,
            dk.ERC20_min_val_sent: self.ERC20_min_val_sent,
            dk.ERC20_max_val_sent: self.ERC20_max_val_sent,
            dk.ERC20_avg_val_sent: self.ERC20_avg_val_sent,
            dk.ERC20_min_val_sent_contract: self.ERC20_min_val_sent_contract,
            dk.ERC20_max_val_sent_contract: self.ERC20_max_val_sent_contract,
            dk.ERC20_avg_val_sent_contract: self.ERC20_avg_val_sent_contract,
            dk.ERC20_uniq_sent_token_name: self.ERC20_uniq_sent_token_name,
            dk.ERC20_uniq_rec_token_name: self.ERC20_uniq_rec_token_name,
            dk.ERC20_most_sent_token_type: self.ERC20_most_sent_token_type,
            dk.ERC20_most_rec_token_type: self.ERC20_most_rec_token_type,
            dk.source: self.source,
        }