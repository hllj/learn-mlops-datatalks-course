import os
from prefect import task, flow, get_run_logger
from datetime import datetime
from dateutil.relativedelta import relativedelta

from src import process_data, train

RAW_DATA_PATH = './data'
DEST_PATH = './output'

@task
def get_paths(date: str, raw_data_path: str, dataset: str):
    if date:
        processed_date = datetime.strptime(date, "%Y-%m-%d")
    else:
        processed_date = datetime.today()
    train_date = processed_date - relativedelta(months=2)
    val_date = processed_date - relativedelta(months=1)
    test_date = processed_date
    train_path = os.path.join(raw_data_path, f"{dataset}_tripdata_{train_date.year}-{str(train_date.month).zfill(2)}.parquet")
    val_path = os.path.join(raw_data_path, f"{dataset}_tripdata_{val_date.year}-{str(val_date.month).zfill(2)}.parquet")
    test_path = os.path.join(raw_data_path, f"{dataset}_tripdata_{test_date.year}-{str(test_date.month).zfill(2)}.parquet")
    return train_path, val_path, test_path

@task
def prepare_data(train_path: str, val_path: str, test_path: str, dest_path: str = './output', date: str = None):
    process_data.run(train_path, val_path, test_path, dest_path=dest_path, date=date)

@task
def train_model(dest_path: str = './output', date: str = None):
    rf = train.run(dest_path, date)
    return rf

@flow
def main(date=None):
    train_path, val_path, test_path = get_paths(date=date, raw_data_path=RAW_DATA_PATH, dataset='green').result()
    dv = prepare_data(train_path, val_path, test_path, dest_path=DEST_PATH, date=date).result()
    rf = train_model(dest_path=DEST_PATH, date=date).result()

# main()

# test function
date = '2021-03-01'
main(date)