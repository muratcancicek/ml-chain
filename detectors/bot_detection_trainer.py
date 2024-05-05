
from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score, auc
from sklearn.metrics import accuracy_score
from sklearn.utils import class_weight
from datetime import datetime
import tensorflowjs as tfjs
import tensorflow as tf
from math import sqrt
import numpy as np
import json

from detectors.experiment_data_handler import ExperimentDataHandler

class BotDetectionTrainer:
    def __init__(self, path_prefix: str = ''):
        self.__path_prefix = path_prefix
        self.__data_handler = ExperimentDataHandler(path_prefix)
        
    def __get_model(self, n_features):
        model = tf.keras.Sequential()
        Dense = tf.keras.layers.Dense
        model.add(Dense(64, input_shape=(n_features,), activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(
            loss='binary_crossentropy',
            optimizer='adam', 
            metrics=['accuracy'],
            )
        return model

    def __train_model(self, train_x, train_y):
        model = self.__get_model(train_x.shape[1])
        class_weights = class_weight.compute_class_weight(
            class_weight = 'balanced', 
            classes = np.unique(train_y),
            y = train_y.flatten(),
        )
        class_weights = dict(enumerate(class_weights))
        model.fit(
            train_x, 
            train_y, 
            epochs=2, 
            batch_size=32, 
            class_weight=class_weights,
        )
        return model

    def __evaluate_model(self, train_x, train_y, test_x, test_y):
        model = self.__train_model(train_x, train_y)
        predictions = model.predict(test_x)
        predictions = [1 if p > 0.5 else 0 for p in predictions]
        accuracy = accuracy_score(test_y, predictions)
        tn, fp, fn, tp = confusion_matrix(test_y, predictions).ravel()
        fpr, tpr, _ = roc_curve(test_y, predictions)
        auc_pr = auc(fpr, tpr)
        auc_roc = roc_auc_score(test_y, predictions)
        return accuracy, tn, fp, fn, tp, auc_pr, auc_roc

    def __calculate_mcc(self, tp, tn, fp, fn):
        numerator = tp * tn - fp * fn
        denominator = sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
        mcc = numerator / denominator if denominator else 0
        return mcc
    
    def __calculate_cohen_kappa(self, tn, fp, fn, tp):
        total = tp + fp + fn + tn
        p0 = (tp + tn) / total
        pe = ((tp + fp) * (tp + fn) + (tn + fp) * (tn + fn)) / (total * total)
        kappa = (p0 - pe) / (1 - pe)
        return kappa

    def __calculate_scores(self, metrics):
        _, tn, fp, fn, tp, _, _ = metrics
        balanced_accuracy = (tp / (tp + fn) + tn / (tn + fp)) / 2
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1_score = 2 * (precision * recall) / (precision + recall)
        mcc = self.__calculate_mcc(tp, tn, fp, fn)
        cohen_kappa = self.__calculate_cohen_kappa(tn, fp, fn, tp)
        g_mean = sqrt((tp / (tp + fn)) * (tn / (tn + fp)))
        return balanced_accuracy, precision, recall, f1_score, mcc, \
            cohen_kappa, g_mean

    def __print_metrics(self, metrics):
        accuracy, tn, fp, fn, tp, auc_pr, auc_roc = metrics
        balanced_accuracy, precision, recall, f1_score, mcc, \
            cohen_kappa, g_mean = self.__calculate_scores(metrics)
        print(f"Accuracy: {accuracy:.2f}")
        print(f"Balanced Accuracy: {balanced_accuracy:.2f}")
        print(f"Precision: {precision:.2f}")
        print(f"Recall: {recall:.2f}")
        print(f"F1 Score: {f1_score:.2f}")
        print(f"AUC-ROC: {auc_roc:.2f}")
        print(f"AUC-PR: {auc_pr:.2f}")
        print(f"MCC: {mcc:.2f}")
        print(f"Cohen's Kappa: {cohen_kappa:.2f}")
        print(f"G-Mean: {g_mean:.2f}")
        print(f"True negatives: {tn}")
        print(f"False positives: {fp}")
        print(f"False negatives: {fn}")
        print(f"True positives: {tp}")
        return

    def evaluate_bot_detection(self):
        metrics = []
        fold_sets = self.__data_handler.prepare_fold_sets()
        for set_ in fold_sets:
            m = self.__evaluate_model(*set_)
            metrics.append(m)
        metrics = np.array(metrics).mean(axis=0)
        self.__print_metrics(metrics)

    def save_bot_detection_model(self):
        set = self.__data_handler.prepare_complete_training_data()
        train_x, train_y, scaling_mean, scaling_std = set
        model = self.__train_model(train_x, train_y)
        now_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        path = f'{self.__path_prefix}data/BotDetectionModel_{now_str}'
        tfjs.converters.save_keras_model(model, path)
        scaler = {'mean': list(scaling_mean), 'std': list(scaling_std)}
        with open(f'{path}/scaler.json', 'w') as f:
            json.dump(scaler, f)
        return