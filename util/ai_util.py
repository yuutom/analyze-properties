import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score
from util.csv_and_pd_util import csv_and_pd_util_class


class ai_util_class:
    def create_model(self):
        csv_and_pd_util = csv_and_pd_util_class()
        X, y = csv_and_pd_util.get_train_and_test_data()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0, shuffle=True)
        model = RandomForestRegressor(random_state=0)
        model.fit(X_train, y_train)
        print('-----------------------------')
        print('score(train data):')
        print(model.score(X=X_train, y=y_train))
        print('score(test data):')
        print(model.score(X=X_test, y=y_test))
        print('-----------------------------')
        return model, X
    
    def predict_rent(self, model, df):
        pred = model.predict(df)
        pred_series = pd.Series(pred, name="予測家賃")
        print('-----------------------------')
        print('予測家賃出力')
        print(pred_series)
        print('-----------------------------')
        return pred_series