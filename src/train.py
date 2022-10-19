import argparse
import os
import pickle

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from prefect import task

import mlflow

from src.process_data import process_data
from src.utils import dump_pickle, load_pickle

@task
def train(train_path: str = '', val_path: str = '', test_path: str = '', data_path: str = '', date: str = ''):
    mlflow.set_tracking_uri("http://127.0.0.1:3499")
    mlflow.set_experiment("nyc-taxi-exp")
    mlflow.sklearn.autolog()
    dv = process_data(train_path, val_path, test_path, data_path, date)
    X_train, y_train = load_pickle(os.path.join(data_path, f"train-{date}.pkl"))
    X_valid, y_valid = load_pickle(os.path.join(data_path, f"valid-{date}.pkl"))
    with mlflow.start_run():
        rf = RandomForestRegressor(max_depth=10, random_state=0)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_valid)
        rmse = mean_squared_error(y_valid, y_pred, squared=False)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_param('date', date)
        mlflow.log_artifact(os.path.join(data_path, f"dv-{date}.pkl"), artifact_path='process')
    dump_pickle(rf, os.path.join(data_path, f"model-{date}.pkl"))
    return dv, rf