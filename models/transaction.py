from utils.costum_keys import CustomKeys as ck

class Transaction(object): 
    def __init__(self, account_address: str, **kwargs):
        self.__init__from_dict(**kwargs)
        self.account_address = account_address
        self.is_received = self.to_address == account_address
        self.is_sent = self.from_address == account_address
        self.is_transfer = self.value != 0
        self.is_contract_creation = self.receipt_contract_address is not None

    def __init__from_dict(self, **kwargs):
        self.__fields = { **kwargs }
        self.hash = kwargs[ck.HASH]
        self.nonce = kwargs[ck.NONCE]
        self.transaction_index = kwargs[ck.TRANSACTION_INDEX]
        self.from_address = kwargs[ck.FROM_ADDRESS]
        self.to_address = kwargs[ck.TO_ADDRESS]
        self.to_address_label = kwargs[ck.TO_ADDRESS_LABEL]
        self.value = float(kwargs[ck.VALUE]) / 10**18
        self.gas = kwargs[ck.GAS]
        self.gas_price = float(kwargs[ck.GAS_PRICE])
        self.input = kwargs[ck.INPUT]
        self.receipt_cumulative_gas_used = kwargs[ck.RECEIPT_CUMULATIVE_GAS_USED]
        self.receipt_gas_used = kwargs[ck.RECEIPT_GAS_USED]
        self.receipt_contract_address = kwargs[ck.RECEIPT_CONTRACT_ADDRESS]
        self.receipt_root = kwargs[ck.RECEIPT_ROOT]
        self.receipt_status = kwargs[ck.RECEIPT_STATUS]
        self.block_timestamp = kwargs[ck.BLOCK_TIMESTAMP]
        self.block_number = kwargs[ck.BLOCK_NUMBER]
        self.block_hash = kwargs[ck.BLOCK_HASH]
        self.transfer_index = kwargs[ck.TRANSFER_INDEX]
        self.erc20_code = kwargs[ck.ERC20_CODE]
        self.is_erc20 = kwargs[ck.IS_ERC20]
        self.erc20_function = kwargs[ck.ERC20_FUNCTION]
        return

    def __getitem__(self, key):
        try:
            return self.__fields[key]
        except KeyError:
            raise KeyError(f"The key '{key}' was not found in the metadata.")
