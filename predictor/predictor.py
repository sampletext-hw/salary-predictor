import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from pandas._typing import NDFrameT
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.tree import DecisionTreeRegressor
import json

class Predictor:

    def get_trained_rf_regressor(self, X_train, y_train):
        # Create a Random Forest regressor
        rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_regressor.fit(X_train, y_train)
        return rf_regressor

    def get_trained_lr_regressor(self, X_train, y_train):
        # Create a Random Forest regressor
        lr_regressor = LinearRegression()
        lr_regressor.fit(X_train, y_train)
        return lr_regressor

    def get_trained_dt_regressor(self, X_train, y_train):
        # Create a Random Forest regressor
        dt_regressor = DecisionTreeRegressor(random_state=1)
        dt_regressor.fit(X_train, y_train)
        return dt_regressor

    def label_transform(self, column: Series | DataFrame | NDFrameT):
        le = LabelEncoder()
        le.fit(column)
        result = le.transform(column)
        label_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
        for key in label_mapping.keys():
            label_mapping[key] = str(label_mapping[key])
        print(json.dumps(label_mapping))
        return result

    def preprocess_data(self, data: DataFrame):
        data.isnull().sum()

        data['Age'] = data['Age'].fillna(data['Age'].mean())
        data['Years of Experience'] = data['Years of Experience'].fillna(data['Years of Experience'].mean())
        data['Salary'] = data['Salary'].fillna(data['Salary'].mean())

        data.isnull().sum()

        data['Gender'] = self.label_transform(data['Gender'])

        data['Education Level'] = data['Education Level'].str.lower()
        data['Education Level'] = data['Education Level'].str.replace(' degree', '')
        data['Education Level'] = self.label_transform(data['Education Level'])

        data['Job Title'] = data['Job Title'].str.lower()
        data['Job Title'] = data['Job Title'].str.replace('junior ', '')
        data['Job Title'] = data['Job Title'].str.replace(' junior', '')
        data['Job Title'] = data['Job Title'].str.replace('senior ', '')
        data['Job Title'] = data['Job Title'].str.replace(' senior', '')
        data['Job Title'] = self.label_transform(data['Job Title'])

        # Select the features and target variable
        feature_columns = ['Age', 'Gender', 'Education Level', 'Job Title', 'Years of Experience']
        target_column = 'Salary'

        X = data[feature_columns]
        y = data[target_column]

        return X, y

    def get_data(self):
        data = pd.read_csv('data.csv')
        print('MEAN SALARY: ', data['Salary'].mean())
        print()

        X, y = self.preprocess_data(data)

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

        return data, X_train, X_test, y_train, y_test

    def make_scaled(self, data):
        Sc_data = data.copy()

        # Проведем те же манипуляции с данными
        X_scaled = Sc_data.drop(columns="Salary")
        y_scaled = Sc_data["Salary"]

        # Скейлим данные
        Scaler = StandardScaler()
        X_scaled = Scaler.fit_transform(X_scaled)

        # Снова разделим выборки
        X_train_s, X_test_s, y_train_s, y_test_s = train_test_split(X_scaled, y_scaled, test_size=0.1)
        return X_train_s, X_test_s, y_train_s, y_test_s

    def get_regressor_accuracy(self, regressor, X_test, y_test):
        return regressor.score(X_test, y_test)

    def print_regressor_stats(self, name, regressor, X_test, y_test, prediction):

        print(name, "MAE: ", mean_absolute_error(y_test, prediction))
        print(name, "RMSE: ", np.sqrt(mean_squared_error(y_test, prediction)))
        rf_score = self.get_regressor_accuracy(regressor, X_test, y_test)
        print(name, "Accuracy: ", rf_score)

        print()

    def find_best_regressor(self, regressors, X_test, y_test):
        best_regressor_name, best_regressor = "", None
        best_accuracy = 0.0

        for regressor_name, regressor in regressors:
            accuracy = self.get_regressor_accuracy(regressor, X_test, y_test)
            if accuracy > best_accuracy:
                best_regressor = regressor
                best_regressor_name = regressor_name
                best_accuracy = accuracy

        return best_regressor_name, best_regressor, best_accuracy

    def __init__(self):
        data, X_train, X_test, y_train, y_test = self.get_data()

        # Посмотрим на корреляции в данных
        print('Correlation')
        print(data.corr()["Salary"].sort_values())
        print()

        rf_regressor = self.get_trained_rf_regressor(X_train, y_train)
        lr_regressor = self.get_trained_lr_regressor(X_train, y_train)
        dt_regressor = self.get_trained_dt_regressor(X_train, y_train)

        rf_predict = rf_regressor.predict(X_test)
        lr_predict = lr_regressor.predict(X_test)
        dt_predict = dt_regressor.predict(X_test)

        self.print_regressor_stats("RF", rf_regressor, X_test, y_test, rf_predict)
        self.print_regressor_stats("LR", lr_regressor, X_test, y_test, lr_predict)
        self.print_regressor_stats("DT", dt_regressor, X_test, y_test, dt_predict)

        regressors = [
            ("RF", rf_regressor),
            ("LR", lr_regressor),
            ("DT", dt_regressor)
        ]
        best_regressor_name, best_regressor, best_accuracy = self.find_best_regressor(regressors, X_test, y_test)

        print("Best Regressor: ", best_regressor_name)
        print("Best Accuracy: ", best_accuracy)
        print()

        # Снова разделим выборки
        X_train_s, X_test_s, y_train_s, y_test_s = self.make_scaled(data)

        # Create a Random Forest regressor
        rf_regressor_s = self.get_trained_rf_regressor(X_train_s, y_train_s)
        lr_regressor_s = self.get_trained_lr_regressor(X_train_s, y_train_s)
        dt_regressor_s = self.get_trained_dt_regressor(X_train_s, y_train_s)

        rf_predict_s = rf_regressor_s.predict(X_test_s)
        lr_predict_s = lr_regressor_s.predict(X_test_s)
        dt_predict_s = dt_regressor_s.predict(X_test_s)

        self.print_regressor_stats("RF Scaled", rf_regressor_s, X_test_s, y_test_s, rf_predict_s)
        self.print_regressor_stats("LR Scaled", lr_regressor_s, X_test_s, y_test_s, lr_predict_s)
        self.print_regressor_stats("DT Scaled", dt_regressor_s, X_test_s, y_test_s, dt_predict_s)

        regressors = [
            ("RF Scaled", rf_regressor_s),
            ("LR Scaled", lr_regressor_s),
            ("DT Scaled", dt_regressor_s)
        ]

        best_regressor_name, best_regressor, best_accuracy = self.find_best_regressor(regressors, X_test_s, y_test_s)

        print("Best Regressor Scaled: ", best_regressor_name)
        print("Best Accuracy Scaled: ", best_accuracy)


        regressors = [
            ("RF", rf_regressor),
            ("LR", lr_regressor),
            ("DT", dt_regressor)
        ]
        best_regressor_name, best_regressor, best_accuracy = self.find_best_regressor(regressors, X_test, y_test)
        self.regressor = best_regressor
        self.accuracy = best_accuracy


if __name__ == "__main__":
    Predictor()
