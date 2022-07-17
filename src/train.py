import argparse
import os
import pickle

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from prefect import task

import mlflow

mlflow.set_tracking_uri("http://127.0.0.1:3499")
mlflow.set_experiment("nyc-taxi-exp")
mlflow.sklearn.autolog()

def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@task
def train(data_path: str, date: str):
    with mlflow.start_run():
        X_train, y_train = load_pickle(os.path.join(data_path, f"train-{date}.pkl"))
        X_valid, y_valid = load_pickle(os.path.join(data_path, f"valid-{date}.pkl"))

        rf = RandomForestRegressor(max_depth=10, random_state=0)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_valid)

        rmse = mean_squared_error(y_valid, y_pred, squared=False)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_param('date', date)
    return rf