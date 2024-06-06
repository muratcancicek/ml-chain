from datetime import datetime

class TransactionHistoryHandler(object):
    def __init__(self, transactions: list):
        self.__filter_transactions(transactions)
        
    def __filter_erc20_transactions(self, transactions: list):
        tnxs = [t for t in transactions if t.is_erc20]
        self.__erc20_len = len(tnxs)
        self.__erc20_sent_transactions = [t for t in tnxs if t.is_sent]
        self.__erc20_received_transactions = [t for t in tnxs if t.is_received]
        cont_trans = [t for t in tnxs if t.is_contract_creation]
        self.__erc20_contract_transactions = cont_trans
        return
        
    def __filter_transactions(self, transactions: list):
        tnxs = sorted(transactions, key=lambda x: x.block_timestamp) 
        self.__transactions = tnxs
        self.__total_len = len(tnxs)
        transfers = [t for t in tnxs if t.is_transfer]
        self.__transfers = transfers
        self.__len = len(self.__transfers)
        self.__sent_transactions = [t for t in transfers if t.is_sent]
        self.__received_transactions = [t for t in transfers if t.is_received]
        cont_trans = [t for t in tnxs if t.is_contract_creation]
        self.__contract_transactions = cont_trans
        self.__filter_erc20_transactions(tnxs)
        return
        
    def __calculate_avg_min_between_tnx(self, transactions: list):
        if len(transactions) < 2:
            return 0
        dates = [t.block_timestamp for t in transactions]
        _format = '%Y-%m-%dT%H:%M:%S.%fZ'
        dates = [datetime.strptime(date, _format) for date in dates]
        _range = range(1, len(dates))
        diffs = [(dates[i] - dates[i - 1]).seconds for i in _range]
        avg = sum(diffs) / len(diffs) 
        return avg / 60

    def calculate_avg_min_between_sent_tnx(self):
        return self.__calculate_avg_min_between_tnx(self.__sent_transactions)

    def calculate_avg_min_between_received_tnx(self):
        a = self.__calculate_avg_min_between_tnx(self.__received_transactions)
        return a

    def __calculate_time_diff_between_first_and_last_mins(self, tnxs: list):
        if len(tnxs) < 2:
            return 0
        first, last = tnxs[0].block_timestamp, tnxs[-1].block_timestamp
        _format = '%Y-%m-%dT%H:%M:%S.%fZ'
        dates = [datetime.strptime(date, _format) for date in [first, last]]
        return (dates[-1] - dates[0]).seconds / 60

    def calculate_time_diff_between_first_and_last_mins(self):
        tnxs = self.__transactions
        return self.__calculate_time_diff_between_first_and_last_mins(tnxs)

    def calculate_sent_tnx(self):
        return len(self.__sent_transactions)

    def calculate_received_tnx(self):
        return len(self.__received_transactions)

    def calculate_number_of_created_contracts(self):
        conts = set(self.__contract_transactions)
        return len(conts)

    def __calculate_unique_received_from_addresses(self, transactions: list):
        return len(set([t.from_address for t in transactions]))

    def calculate_unique_received_from_addresses(self):
        return self.__calculate_unique_received_from_addresses(
            self.__received_transactions,
            )
    
    def __calculate_unique_sent_to_addresses(self, transactions: list):
        return len(set([t.to_address for t in transactions]))
    
    def calculate_unique_sent_to_addresses(self):
        return self.__calculate_unique_sent_to_addresses(
            self.__sent_transactions,
            )

    def __calculate_min_value(self, transactions: list):
        if not transactions:
            return 0
        return min([t.value for t in transactions])

    def calculate_min_value_received(self):
        return self.__calculate_min_value(self.__received_transactions)
    
    def __calculate_max_value(self, transactions: list):
        if not transactions:
            return 0
        return max([t.value for t in transactions])
    
    def calculate_max_value_received(self):
        return self.__calculate_max_value(self.__received_transactions)

    def __calculate_avg_value(self, transactions: list):
        if not transactions:
            return 0
        _sum = sum([t.value for t in transactions])
        return _sum / len(transactions)

    def calculate_avg_val_received(self):
        return self.__calculate_avg_value(self.__received_transactions)

    def calculate_min_val_sent(self):
        return self.__calculate_min_value(self.__sent_transactions)

    def calculate_max_val_sent(self):
        return self.__calculate_max_value(self.__sent_transactions)

    def calculate_avg_val_sent(self):
        return self.__calculate_avg_value(self.__sent_transactions)

    def calculate_min_value_sent_to_contract(self):
        return self.__calculate_min_value(self.__contract_transactions)
    
    def calculate_max_val_sent_to_contract(self):
        return self.__calculate_max_value(self.__contract_transactions)

    def calculate_avg_value_sent_to_contract(self):
        return self.__calculate_avg_value(self.__contract_transactions)

    def calculate_total_transactions_including_tnx_to_create_contract(self):
        return self.__total_len

    def calculate_total_ether_sent(self):
        return sum([t.value for t in self.__sent_transactions])

    def calculate_total_ether_received(self):
        return sum([t.value for t in self.__received_transactions])

    def calculate_total_ether_sent_contracts(self):
        return sum([t.value for t in self.__contract_transactions])

    def calculate_total_ether_balance(self):
        received = self.calculate_total_ether_received()
        sent = self.calculate_total_ether_sent()
        return received - sent

    def calculate_total_ERC20_tnxs(self):
        return self.__erc20_len

    def calculate_ERC20_total_ether_received(self):
        return sum([t.value for t in self.__erc20_received_transactions])
    
    def calculate_ERC20_total_ether_sent(self):
        return sum([t.value for t in self.__erc20_sent_transactions])
    
    def calculate_ERC20_total_ether_sent_contract(self):
        return sum([t.value for t in self.__erc20_contract_transactions])

    def calculate_ERC20_uniq_sent_addr(self):
        return self.__calculate_unique_sent_to_addresses(
            self.__erc20_sent_transactions,
            )
    
    def calculate_ERC20_uniq_rec_addr(self):
        return self.__calculate_unique_received_from_addresses(
            self.__erc20_received_transactions,
            )
    
    def calculate_ERC20_uniq_sent_addr_1(self):
        return self.calculate_ERC20_uniq_sent_addr()
    
    def calculate_ERC20_uniq_rec_contract_addr(self):
        s = set([t.from_address for t in self.__erc20_contract_transactions])
        return len(s)
    
    def calculate_ERC20_avg_time_between_sent_tnx(self):
        return self.__calculate_avg_min_between_tnx(
            self.__erc20_sent_transactions,
            )
    
    def calculate_ERC20_avg_time_between_rec_tnx(self):
        return self.__calculate_avg_min_between_tnx(
            self.__erc20_received_transactions,
            )

    def calculate_ERC20_avg_time_between_rec_2_tnx(self):
        return self.calculate_ERC20_avg_time_between_rec_tnx()

    def calculate_ERC20_avg_time_between_contract_tnx(self):
        return self.__calculate_avg_min_between_tnx(
            self.__erc20_contract_transactions,
            )

    def calculate_ERC20_min_val_rec(self):
        return self.__calculate_min_value(self.__erc20_received_transactions)

    def calculate_ERC20_max_val_rec(self):
        return self.__calculate_max_value(self.__erc20_received_transactions)

    def calculate_ERC20_avg_val_rec(self):
        return self.__calculate_avg_value(self.__erc20_received_transactions)

    def calculate_ERC20_min_val_sent(self):
        return self.__calculate_min_value(self.__erc20_sent_transactions)

    def calculate_ERC20_max_val_sent(self):
        return self.__calculate_max_value(self.__erc20_sent_transactions)

    def calculate_ERC20_avg_val_sent(self):
        return self.__calculate_avg_value(self.__erc20_sent_transactions)
    
    def calculate_ERC20_min_val_sent_contract(self):
        return self.__calculate_min_value(self.__erc20_contract_transactions)

    def calculate_ERC20_max_val_sent_contract(self):
        return self.__calculate_max_value(self.__erc20_contract_transactions)

    def calculate_ERC20_avg_val_sent_contract(self):
        return self.__calculate_avg_value(self.__erc20_contract_transactions)

    def calculate_ERC20_uniq_sent_token_name(self):
        return len(set([t.input[:10] for t in self.__erc20_sent_transactions]))

    def calculate_ERC20_uniq_rec_token_name(self):
        s = set([t.input[:10] for t in self.__erc20_received_transactions])
        return len(s)

    def calculate_ERC20_most_sent_token_type(self):
        if not self.__erc20_sent_transactions:
            return ''
        s = [t.input[:10] for t in self.__erc20_sent_transactions]
        return max(set(s), key=s.count)

    def calculate_ERC20_most_rec_token_type(self):
        if not self.__erc20_received_transactions:
            return ''
        s = [t.input[:10] for t in self.__erc20_received_transactions]
        return max(set(s), key=s.count)


