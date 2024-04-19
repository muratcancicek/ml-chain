from data_handler.transaction_history_handler import TransactionHistoryHandler
from utils.costum_keys import CustomKeys as ck

class Account(object): 
    def __init__(self, from_dataset: bool = False, **kwargs):
        if from_dataset:
            self.__init__from_dataset(**kwargs)
        else:
            self.__init__from_history(**kwargs)

    def __init__from_dataset(self, **kwargs):
        self.__fields = { **kwargs }
        self.address = kwargs[ck.ADDRESS]
        self.FLAG = kwargs[ck.FLAG]
        self.avg_min_between_sent_tnx = kwargs[ck.AVG_MIN_BETWEEN_RECEIVED_TNX]
        self.avg_min_between_received_tnx = kwargs[ck.AVG_MIN_BETWEEN_RECEIVED_TNX]
        self.time_diff_between_first_and_last_mins = kwargs[ck.TIME_DIFF_BETWEEN_FIRST_AND_LAST_MINS]
        self.sent_tnx = kwargs[ck.SENT_TNX]
        self.received_tnx = kwargs[ck.RECEIVED_TNX]
        self.number_of_created_contracts = kwargs[ck.NUMBER_OF_CREATED_CONTRACTS]
        self.unique_received_from_addresses = kwargs[ck.UNIQUE_RECEIVED_FROM_ADDRESSES]
        self.unique_sent_to_addresses = kwargs[ck.UNIQUE_SENT_TO_ADDRESSES]
        self.min_value_received = kwargs[ck.MIN_VALUE_RECEIVED]
        self.max_value_received = kwargs[ck.MAX_VALUE_RECEIVED]
        self.avg_val_received = kwargs[ck.AVG_VAL_RECEIVED]
        self.min_val_sent = kwargs[ck.MIN_VAL_SENT]
        self.max_val_sent = kwargs[ck.MAX_VAL_SENT]
        self.avg_val_sent = kwargs[ck.AVG_VAL_SENT]
        self.min_value_sent_to_contract = kwargs[ck.MIN_VALUE_SENT_TO_CONTRACT]
        self.max_val_sent_to_contract = kwargs[ck.MAX_VAL_SENT_TO_CONTRACT]
        self.avg_value_sent_to_contract = kwargs[ck.AVG_VALUE_SENT_TO_CONTRACT]
        self.total_transactions_including_tnx_to_create_contract = kwargs[ck.TOTAL_TRANSACTIONS_INCLUDING_TNX_TO_CREATE_CONTRACT]
        self.total_ether_sent = kwargs[ck.TOTAL_ETHER_SENT]
        self.total_ether_received = kwargs[ck.TOTAL_ETHER_RECEIVED]
        self.total_ether_sent_contracts = kwargs[ck.TOTAL_ETHER_SENT_CONTRACTS]
        self.total_ether_balance = kwargs[ck.TOTAL_ETHER_BALANCE]
        self.total_ERC20_tnxs = kwargs[ck.TOTAL_ERC20_TNXS]
        self.ERC20_total_ether_received = kwargs[ck.ERC20_TOTAL_ETHER_RECEIVED]
        self.ERC20_total_ether_sent = kwargs[ck.ERC20_TOTAL_ETHER_SENT]
        self.ERC20_total_ether_sent_contract = kwargs[ck.ERC20_TOTAL_ETHER_SENT_CONTRACT]
        self.ERC20_uniq_sent_addr = kwargs[ck.ERC20_UNIQ_SENT_ADDR]
        self.ERC20_uniq_rec_addr = kwargs[ck.ERC20_UNIQ_REC_ADDR]
        self.ERC20_uniq_sent_addr_1 = kwargs[ck.ERC20_UNIQ_SENT_ADDR_1]
        self.ERC20_uniq_rec_contract_addr = kwargs[ck.ERC20_UNIQ_REC_CONTRACT_ADDR]
        self.ERC20_avg_time_between_sent_tnx = kwargs[ck.ERC20_AVG_TIME_BETWEEN_SENT_TNX]
        self.ERC20_avg_time_between_rec_tnx = kwargs[ck.ERC20_AVG_TIME_BETWEEN_REC_TNX]
        self.ERC20_avg_time_between_rec_2_tnx = kwargs[ck.ERC20_AVG_TIME_BETWEEN_REC_2_TNX]
        self.ERC20_avg_time_between_contract_tnx = kwargs[ck.ERC20_AVG_TIME_BETWEEN_CONTRACT_TNX]
        self.ERC20_min_val_rec = kwargs[ck.ERC20_MIN_VAL_REC]
        self.ERC20_max_val_rec = kwargs[ck.ERC20_MAX_VAL_REC]
        self.ERC20_avg_val_rec = kwargs[ck.ERC20_AVG_VAL_REC]
        self.ERC20_min_val_sent = kwargs[ck.ERC20_MIN_VAL_SENT]
        self.ERC20_max_val_sent = kwargs[ck.ERC20_MAX_VAL_SENT]
        self.ERC20_avg_val_sent = kwargs[ck.ERC20_AVG_VAL_SENT]
        self.ERC20_min_val_sent_contract = kwargs[ck.ERC20_MIN_VAL_SENT_CONTRACT]
        self.ERC20_max_val_sent_contract = kwargs[ck.ERC20_MAX_VAL_SENT_CONTRACT]
        self.ERC20_avg_val_sent_contract = kwargs[ck.ERC20_AVG_VAL_SENT_CONTRACT]
        self.ERC20_uniq_sent_token_name = kwargs[ck.ERC20_UNIQ_SENT_TOKEN_NAME]
        self.ERC20_uniq_rec_token_name = kwargs[ck.ERC20_UNIQ_REC_TOKEN_NAME]
        self.ERC20_most_sent_token_type = kwargs[ck.ERC20_MOST_SENT_TOKEN_TYPE]
        self.ERC20_most_rec_token_type = kwargs[ck.ERC20_MOST_REC_TOKEN_TYPE]
        self.label_source = kwargs[ck.LABEL_SOURCE]
        if ck.DATA_SOURCE in kwargs:
            self.data_source = kwargs[ck.DATA_SOURCE]
        else:
            self.data_source = kwargs[ck.LABEL_SOURCE]
        return
    
    def __init__from_history(self, **kwargs):
        self.__fields = { **kwargs }
        self.address = kwargs[ck.ADDRESS]
        self.FLAG = kwargs[ck.FLAG]
        self.label_source = kwargs[ck.LABEL_SOURCE]
        if ck.DATA_SOURCE in kwargs:
            self.data_source = kwargs[ck.DATA_SOURCE]
        else:
            self.data_source = kwargs[ck.LABEL_SOURCE]
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
            ck.ADDRESS: self.address,
            ck.FLAG: self.FLAG,
            ck.AVG_MIN_BETWEEN_SENT_TNX: self.avg_min_between_sent_tnx,
            ck.AVG_MIN_BETWEEN_RECEIVED_TNX: self.avg_min_between_received_tnx,
            ck.TIME_DIFF_BETWEEN_FIRST_AND_LAST_MINS: self.time_diff_between_first_and_last_mins,
            ck.SENT_TNX: self.sent_tnx,
            ck.RECEIVED_TNX: self.received_tnx,
            ck.NUMBER_OF_CREATED_CONTRACTS: self.number_of_created_contracts,
            ck.UNIQUE_RECEIVED_FROM_ADDRESSES: self.unique_received_from_addresses,
            ck.UNIQUE_SENT_TO_ADDRESSES: self.unique_sent_to_addresses,
            ck.MIN_VALUE_RECEIVED: self.min_value_received,
            ck.MAX_VALUE_RECEIVED: self.max_value_received,
            ck.AVG_VAL_RECEIVED: self.avg_val_received,
            ck.MIN_VAL_SENT: self.min_val_sent,
            ck.MAX_VAL_SENT: self.max_val_sent,
            ck.AVG_VAL_SENT: self.avg_val_sent,
            ck.MIN_VALUE_SENT_TO_CONTRACT: self.min_value_sent_to_contract,
            ck.MAX_VAL_SENT_TO_CONTRACT: self.max_val_sent_to_contract,
            ck.AVG_VALUE_SENT_TO_CONTRACT: self.avg_value_sent_to_contract,
            ck.TOTAL_TRANSACTIONS_INCLUDING_TNX_TO_CREATE_CONTRACT: self.total_transactions_including_tnx_to_create_contract,
            ck.TOTAL_ETHER_SENT: self.total_ether_sent,
            ck.TOTAL_ETHER_RECEIVED: self.total_ether_received,
            ck.TOTAL_ETHER_SENT_CONTRACTS: self.total_ether_sent_contracts,
            ck.TOTAL_ETHER_BALANCE: self.total_ether_balance,
            ck.TOTAL_ERC20_TNXS: self.total_ERC20_tnxs,
            ck.ERC20_TOTAL_ETHER_RECEIVED: self.ERC20_total_ether_received,
            ck.ERC20_TOTAL_ETHER_SENT: self.ERC20_total_ether_sent,
            ck.ERC20_TOTAL_ETHER_SENT_CONTRACT: self.ERC20_total_ether_sent_contract,
            ck.ERC20_UNIQ_SENT_ADDR: self.ERC20_uniq_sent_addr,
            ck.ERC20_UNIQ_REC_ADDR: self.ERC20_uniq_rec_addr,
            ck.ERC20_UNIQ_SENT_ADDR_1: self.ERC20_uniq_sent_addr_1,
            ck.ERC20_UNIQ_REC_CONTRACT_ADDR: self.ERC20_uniq_rec_contract_addr,
            ck.ERC20_AVG_TIME_BETWEEN_SENT_TNX: self.ERC20_avg_time_between_sent_tnx,
            ck.ERC20_AVG_TIME_BETWEEN_REC_TNX: self.ERC20_avg_time_between_rec_tnx,
            ck.ERC20_AVG_TIME_BETWEEN_REC_2_TNX: self.ERC20_avg_time_between_rec_2_tnx,
            ck.ERC20_AVG_TIME_BETWEEN_CONTRACT_TNX: self.ERC20_avg_time_between_contract_tnx,
            ck.ERC20_MIN_VAL_REC: self.ERC20_min_val_rec,
            ck.ERC20_MAX_VAL_REC: self.ERC20_max_val_rec,
            ck.ERC20_AVG_VAL_REC: self.ERC20_avg_val_rec,
            ck.ERC20_MIN_VAL_SENT: self.ERC20_min_val_sent,
            ck.ERC20_MAX_VAL_SENT: self.ERC20_max_val_sent,
            ck.ERC20_AVG_VAL_SENT: self.ERC20_avg_val_sent,
            ck.ERC20_MIN_VAL_SENT_CONTRACT: self.ERC20_min_val_sent_contract,
            ck.ERC20_MAX_VAL_SENT_CONTRACT: self.ERC20_max_val_sent_contract,
            ck.ERC20_AVG_VAL_SENT_CONTRACT: self.ERC20_avg_val_sent_contract,
            ck.ERC20_UNIQ_SENT_TOKEN_NAME: self.ERC20_uniq_sent_token_name,
            ck.ERC20_UNIQ_REC_TOKEN_NAME: self.ERC20_uniq_rec_token_name,
            ck.ERC20_MOST_SENT_TOKEN_TYPE: self.ERC20_most_sent_token_type,
            ck.ERC20_MOST_REC_TOKEN_TYPE: self.ERC20_most_rec_token_type,
            ck.DATA_SOURCE: self.data_source,
            ck.LABEL_SOURCE: self.label_source,
        }
