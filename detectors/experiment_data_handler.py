import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from utils.costum_keys import CustomKeys as ck
from data_handler.meta_data_handler import MetaDataHandler

class ExperimentDataHandler(object):
    def __init__(self, path_prefix: str = ''):
        self.__path_prefix = path_prefix
        self.__metadata_handler = MetaDataHandler("data/experiment.json")
        self.__data = pd.read_csv(f'{self.__path_prefix}data/uxly_dataset.csv')
        self.__columns_to_drop = self.__metadata_handler.get_columns_to_drop()
        self.__base_feature_names = self.__metadata_handler.get_base_features()
        self.__use_base_features = self.__metadata_handler.get_use_base_features()
        self.__positive_flags = self.__metadata_handler.get_positive_flags()
        self.__nagative_flags = self.__metadata_handler.get_negative_flags()

    def __rearange_y_parameters(self,y_sample):
        y_rearanged = np.zeros(len(y_sample))
        for i,value in enumerate(y_sample):
            if(value in self.__nagative_flags):
                y_rearanged[i] = 0.0
            elif(value in self.__positive_flags):
                y_rearanged[i] = 1.0
        return y_rearanged
    
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
        train_y_rearanged = self.__rearange_y_parameters(train_y)
        test_y_rearanged = self.__rearange_y_parameters(test_y)
        return train_x_scaled, train_y_rearanged, test_x_scaled, test_y_rearanged

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
