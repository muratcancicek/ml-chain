import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from utils.costum_keys import CustomKeys as ck

class ExperimentDataHandler(object):
    def __init__(self, path_prefix: str = ''):
        self.__path_prefix = path_prefix
        self.__data = pd.read_csv(f'{self.__path_prefix}data/uxly_dataset.csv')
        self.__columns_to_drop = self.__get_columns_to_drop()
        self.__base_feature_names = self.__get_base_feature_names()
        self.__use_base_features = True
        self.__positive_flags = [ck.KAGGLE_LABELED_BOT_FLAG]
        self.__nagative_flags = [ck.NEGATIVE_FLAG]

    def __get_columns_to_drop(self):
        return [
            ck.ADDRESS, 
            ck.ERC20_MOST_REC_TOKEN_TYPE, 
            ck.ERC20_MOST_SENT_TOKEN_TYPE,
            ck.DATA_SOURCE,
            ck.LABEL_SOURCE,
            ]

    def __get_base_feature_names(self):
        return [
            ck.FLAG,
            ck.AVG_MIN_BETWEEN_SENT_TNX,
            ck.AVG_MIN_BETWEEN_RECEIVED_TNX,
            ck.TIME_DIFF_BETWEEN_FIRST_AND_LAST_MINS,
            ck.SENT_TNX,
            ck.RECEIVED_TNX,
            ck.UNIQUE_RECEIVED_FROM_ADDRESSES,
            ck.UNIQUE_SENT_TO_ADDRESSES,
            ck.MIN_VALUE_RECEIVED,
            ck.MAX_VALUE_RECEIVED,
            ck.AVG_VAL_RECEIVED,
            ck.MIN_VAL_SENT,
            ck.MAX_VAL_SENT,
            ck.AVG_VAL_SENT,
            ck.TOTAL_TRANSACTIONS_INCLUDING_TNX_TO_CREATE_CONTRACT,
            ck.TOTAL_ETHER_SENT,
            ck.TOTAL_ETHER_RECEIVED,
            ck.TOTAL_ETHER_BALANCE,            
        ]

    def __filter_data(self):
        df = self.__data.drop(columns=self.__columns_to_drop).astype(np.float64)
        if self.__use_base_features:
            df = df[self.__base_feature_names]
        df = df.dropna()
        return df

    def __get_labeled_samples(self, randomize: bool = True):
        df = self.__filter_data()
        negative_samples = df[df[ck.FLAG].isin(self.__nagative_flags)]
        positive_samples = df[df[ck.FLAG].isin(self.__positive_flags)]
        if randomize:
            negative_samples = negative_samples.sample(frac=1)
            positive_samples = positive_samples.sample(frac=1)
        return negative_samples.values, positive_samples.values

    def __split_folds(self, randomize: bool = True):
        negatives, positives = self.__get_labeled_samples(randomize)
        positive_folds = np.array_split(positives, 4)
        negative_folds = np.array_split(negatives, 4)
        folds = []
        for i in range(4):
            fold = np.concatenate([positive_folds[i], negative_folds[i]])
            if randomize:
                np.random.shuffle(fold)
            folds.append(fold)
        return folds

    def __prepare_fold_sets(self, training_folds, test_fold):
        test_data = np.copy(test_fold)
        train_data = np.concatenate(training_folds)
        train_x, train_y = train_data[:, 1:], train_data[:, 0]
        test_x, test_y = test_data[:, 1:], test_data[:, 0]
        scaler = StandardScaler()
        train_x_scaled = scaler.fit_transform(train_x)
        test_x_scaled = scaler.transform(test_x)
        return train_x_scaled, train_y, test_x_scaled, test_y

    def prepare_fold_sets(self, randomize: bool = True):
        individual_folds = self.__split_folds(randomize)
        fold_sets = []
        for i, test_fold in enumerate(individual_folds):
            training_folds = \
                [f for j, f in enumerate(individual_folds) if j != i]
            sets = self.__prepare_fold_sets(training_folds, test_fold)
            fold_sets.append(sets)
        return fold_sets

    def prepare_complete_training_data(self, randomize: bool = True):
        negatives, positives = self.__get_labeled_samples(randomize)
        data = np.concatenate([negatives, positives])
        if randomize:
            np.random.shuffle(data)
        x, y = data[:, 1:], data[:, 0]
        scaler = StandardScaler()
        x_scaled = scaler.fit_transform(x)
        return x_scaled, y, scaler.mean_, scaler.scale_
