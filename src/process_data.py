import argparse
import os 
import pickle

import pandas as pd
from sklearn.feature_extraction import DictVectorizer


def dump_pickle(obj, filename):
    with open(filename, "wb") as f_out:
        return pickle.dump(obj, f_out)


def read_dataframe(filename: str):
    df = pd.read_parquet(filename)
    df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.apply(lambda td: td.total_seconds() / 60)
    df = df[(df.duration >= 1) & (df.duration <= 60)]
    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)
    return df

def preprocess(df: pd.DataFrame, dv: DictVectorizer, fit_dv: bool = False):
    df['PU_DO'] = df['PULocationID'] + '_' + df['DOLocationID']
    categorical = ['PU_DO']
    numerical = ['trip_distance']
    dicts = df[categorical + numerical].to_dict(orient='records')
    if fit_dv:
        X = dv.fit_transform(dicts)
    else:
        X = dv.transform(dicts)
    return X, dv

def run(train_path: str = '', val_path: str = '', test_path: str = '', dest_path: str = './output', date: str = ''):
    df_train = read_dataframe(train_path)
    df_val = read_dataframe(val_path)
    df_test = read_dataframe(test_path)

    target = "duration"
    y_train = df_train[target].values
    y_valid = df_val[target].values
    y_test = df_test[target].values

    dv = DictVectorizer()
    X_train, dv = preprocess(df_train, dv, fit_dv=True)
    X_val, _ = preprocess(df_val, dv, fit_dv=False)
    X_test, _ = preprocess(df_test, dv, fit_dv=False)

    os.makedirs(dest_path, exist_ok=True)

    dump_pickle(dv, os.path.join(dest_path, f"dv-{date}.pkl"))
    dump_pickle((X_train, y_train), os.path.join(dest_path, f"train-{date}.pkl"))
    dump_pickle((X_val, y_valid), os.path.join(dest_path, f"valid-{date}.pkl"))
    dump_pickle((X_test, y_test), os.path.join(dest_path, f"test-{date}.pkl"))