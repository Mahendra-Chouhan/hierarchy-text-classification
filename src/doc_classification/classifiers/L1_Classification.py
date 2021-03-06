# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 00:46:34 2019

@author: mahi-1234
"""

from .text_classification import text_classification
import logging
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm
from sklearn.metrics import accuracy_score
import uuid

class l1_classification(text_classification):
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def get_classifier_default_details(self, model_name, model_path, version):
        # retrun the classifier details
        self.model_name = model_name
        self.model_path = model_path
        self.version = version
        classifier_details = text_classification.get_detault_detail(self)
        classifier_details["model_name"] = self.model_name
        classifier_details["model_uuid"] = uuid.uuid4().int
        classifier_details["model_path"] = self.model_path
        classifier_details["version"] = self.version
        classifier_details["description"] = """This is L1 Classifier"""
        classifier_details["child"] = {"sub_classifiers": [],
                                       "lables": []}
        return classifier_details

    def train_and_evaluation(self, csv_dataframe, feature_name, lable_name):
        features = csv_dataframe[feature_name]
        lables = csv_dataframe[lable_name]
        features = list(features)
        lables = list(lables)
        train_x, test_x, train_y, test_y = text_classification.train_test_spliting(self, 
                                                                                   features,
                                                                                   lables)
        model = self.train_classification(train_x, train_y)
        self._save_model(model, self.model_name, self.model_path)
        model = self.load_model(self.model_name, self.model_path)
        evaluation = self.evaluation(model, test_x, test_y)
        return True, evaluation

    def train_classification(self, features, lables):
        logreg = LogisticRegression()
        logreg.fit(features, lables)
        return logreg

    def evaluation(self, model, test_x, test_y):
        y_pred = model.predict(test_x)
        accuracy = accuracy_score(test_y, y_pred)
        self.logger.info("Getting Aurracy: {}".format(accuracy))
        return accuracy

    def _save_model(self, model, model_name, model_path):
        model_path_complete = "{}/{}.pickle".format(model_path, model_name)
        pickle.dump(model, open(model_path_complete, 'wb'))
        self.logger.info("""Model Saved at {}""".format(model_path))

    def load_model(self, model_name, model_path):
        model_path_complete = "{}/{}.pickle".format(model_path, model_name)
        return pickle.load(open(model_path_complete, 'rb'))

    def predict_label(self, para_2_vec):
        model = self.load_model(self.model_name, self.model_path)
        return model.predict(para_2_vec)
