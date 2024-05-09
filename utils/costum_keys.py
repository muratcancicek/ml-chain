
class CustomKeys:
    MORALIS = 'moralis'
    ETHERSCAN = 'etherscan'
    NEGATIVE_FLAG = 0
    KAGGLE_LABELED_BOT_FLAG = 1
    MEV_BOT_FLAG = 2
    SPAM_FLAG = 3
    QUERY_TIME = 'query_time'

    # Account keys
    TRANSACTIONS = 'transactions'
    ADDRESS = 'address'
    FLAG = 'flag'
    LABEL_SOURCE = 'label_source'
    DATA_SOURCE = 'data_source'
    AVG_MIN_BETWEEN_SENT_TNX = 'avg_min_between_sent_tnx'
    AVG_MIN_BETWEEN_RECEIVED_TNX = 'avg_min_between_received_tnx'
    TIME_DIFF_BETWEEN_FIRST_AND_LAST_MINS = 'time_diff_between_first_and_last_mins'
    SENT_TNX = 'sent_tnx'
    RECEIVED_TNX = 'received_tnx'
    NUMBER_OF_CREATED_CONTRACTS = 'number_of_created_contracts'
    UNIQUE_RECEIVED_FROM_ADDRESSES = 'unique_received_from_addresses'
    UNIQUE_SENT_TO_ADDRESSES = 'unique_sent_to_addresses'
    MIN_VALUE_RECEIVED = 'min_value_received'
    MAX_VALUE_RECEIVED = 'max_value_received'
    AVG_VAL_RECEIVED = 'avg_val_received'
    MIN_VAL_SENT = 'min_val_sent'
    MAX_VAL_SENT = 'max_val_sent'
    AVG_VAL_SENT = 'avg_val_sent'
    MIN_VALUE_SENT_TO_CONTRACT = 'min_value_sent_to_contract'
    MAX_VAL_SENT_TO_CONTRACT = 'max_val_sent_to_contract'
    AVG_VALUE_SENT_TO_CONTRACT = 'avg_value_sent_to_contract'
    TOTAL_TRANSACTIONS_INCLUDING_TNX_TO_CREATE_CONTRACT = 'total_transactions_including_tnx_to_create_contract'
    TOTAL_ETHER_SENT = 'total_ether_sent'
    TOTAL_ETHER_RECEIVED = 'total_ether_received'
    TOTAL_ETHER_SENT_CONTRACTS = 'total_ether_sent_contracts'
    TOTAL_ETHER_BALANCE = 'total_ether_balance'
    TOTAL_ERC20_TNXS = 'total_ERC20_tnxs'
    ERC20_TOTAL_ETHER_RECEIVED = 'ERC20_total_ether_received'
    ERC20_TOTAL_ETHER_SENT = 'ERC20_total_ether_sent'
    ERC20_TOTAL_ETHER_SENT_CONTRACT = 'ERC20_total_ether_sent_contract'
    ERC20_UNIQ_SENT_ADDR = 'ERC20_uniq_sent_addr'
    ERC20_UNIQ_REC_ADDR = 'ERC20_uniq_rec_addr'
    ERC20_UNIQ_SENT_ADDR_1 = 'ERC20_uniq_sent_addr_1'
    ERC20_UNIQ_REC_CONTRACT_ADDR = 'ERC20_uniq_rec_contract_addr'
    ERC20_AVG_TIME_BETWEEN_SENT_TNX = 'ERC20_avg_time_between_sent_tnx'
    ERC20_AVG_TIME_BETWEEN_REC_TNX = 'ERC20_avg_time_between_rec_tnx'
    ERC20_AVG_TIME_BETWEEN_REC_2_TNX = 'ERC20_avg_time_between_rec_2_tnx'
    ERC20_AVG_TIME_BETWEEN_CONTRACT_TNX = 'ERC20_avg_time_between_contract_tnx'
    ERC20_MIN_VAL_REC = 'ERC20_min_val_rec'
    ERC20_MAX_VAL_REC = 'ERC20_max_val_rec'
    ERC20_AVG_VAL_REC = 'ERC20_avg_val_rec'
    ERC20_MIN_VAL_SENT = 'ERC20_min_val_sent'
    ERC20_MAX_VAL_SENT = 'ERC20_max_val_sent'
    ERC20_AVG_VAL_SENT = 'ERC20_avg_val_sent'
    ERC20_MIN_VAL_SENT_CONTRACT = 'ERC20_min_val_sent_contract'
    ERC20_MAX_VAL_SENT_CONTRACT = 'ERC20_max_val_sent_contract'
    ERC20_AVG_VAL_SENT_CONTRACT = 'ERC20_avg_val_sent_contract'
    ERC20_UNIQ_SENT_TOKEN_NAME = 'ERC20_uniq_sent_token_name'
    ERC20_UNIQ_REC_TOKEN_NAME = 'ERC20_uniq_rec_token_name'
    ERC20_MOST_SENT_TOKEN_TYPE = 'ERC20_most_sent_token_type'
    ERC20_MOST_REC_TOKEN_TYPE = 'ERC20_most_rec_token_type'

    # Transaction keys
    CURSOR = 'cursor'
    PAGE_SIZE = 'page_size'
    PAGE = 'page'
    RESULT = 'result'
    HASH = 'hash'
    NONCE = 'nonce'
    TRANSACTION_INDEX = 'transaction_index'
    FROM_ADDRESS = 'from_address'
    FROM_ADDRESS_LABEL = 'from_address_label'
    TO_ADDRESS = 'to_address'
    TO_ADDRESS_LABEL = 'to_address_label'
    VALUE = 'value'
    GAS = 'gas'
    GAS_PRICE = 'gas_price'
    INPUT = 'input'
    RECEIPT_CUMULATIVE_GAS_USED = 'receipt_cumulative_gas_used'
    RECEIPT_GAS_USED = 'receipt_gas_used'
    RECEIPT_CONTRACT_ADDRESS = 'receipt_contract_address'
    RECEIPT_ROOT = 'receipt_root'
    RECEIPT_STATUS = 'receipt_status'
    BLOCK_TIMESTAMP = 'block_timestamp'
    BLOCK_NUMBER = 'block_number'
    BLOCK_HASH = 'block_hash'
    TRANSFER_INDEX = 'transfer_index'
    ERC20_SIGNATURES = 'erc20_signatures'
    ERC20_TRANSFER_SIGNATURE = 'erc20_transfer_signature'
    ERC20_TRANSFER_FROM_SIGNATURE = 'erc20_transfer_from_signature'
    ERC20_APPROVE_SIGNATURE = 'erc20_approve_signature'
    ERC20_CODE = 'erc20_code'
    ERC20_FUNCTION = 'erc20_function'
    IS_ERC20 = 'is_erc20'
    
    #Stats Keys
    NFTS = 'nfts'
    COLLECTIONS = 'collections'
    TOTAL = 'total'
    NFT_TRANSFERS = 'nft_transfers'
    TOKEN_TRANSFERS = 'token_transfers'
    TOTAL_TRANSACTIONS = 'total_transactions'
    TOTAL_NFT_TRANSFERS = 'total_nft_transfers'
    TOTAL_TOKEN_TRANSFERS = 'total_token_transfers'
    