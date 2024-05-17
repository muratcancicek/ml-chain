import json
from utils.costum_keys import CustomKeys as ck

class MetaDataHandler:
    def __init__(self,metadata_path : str) -> None:
        self.__metadata = self.read_metadata(metadata_path)
    
    def read_metadata(self,metadata_path : str) -> dict:
        return json.load(open(metadata_path,"r"))
    
    def get_architecture(self):
        return self.__metadata[ck.ARCHITECTURE]
    
    def get_epochs(self):
        return self.__metadata[ck.EPOCHS]
    
    def get_batch_size(self):
        return self.__metadata[ck.BATCH_SIZE]
    
    def get_learning_rate(self):
        return self.__metadata[ck.LEARNING_RATE]
    
    def get_dropout(self):
        return self.__metadata[ck.DROPOUT]
    
    def get_positive_flags(self):
        return self.__metadata[ck.POSITIVE_FLAGS]
    
    def get_negative_flags(self):
        return self.__metadata[ck.NEGATIVE_FLAGS]
    
    def get_use_base_features(self):
        return self.__metadata[ck.USE_BASE_FEATURES]
    
    def get_columns_to_drop(self):
        return self.__metadata[ck.COLUMNS_TO_DROP]
    
    def get_base_features(self):
        return self.__metadata[ck.BASE_FEATURES]
    
    def get_cross_validation_count(self):
        return self.__metadata[ck.CROSS_VALIDATION_COUNT]