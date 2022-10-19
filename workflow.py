import os
from prefect import task, flow, get_run_logger
from datetime import datetime
from dateutil.relativedelta import relativedelta

from src import download_dataset_by_date, process_data, train

RAW_DATA_PATH = './data'
DEST_PATH = './output'

@task
def get_paths(date: str, dataset: str):
    if date:
        processed_date = datetime.strptime(date, "%Y-%m-%d")
    else:
        processed_date = datetime.today()
    train_date = processed_date - relativedelta(months=2)
    val_date = processed_date - relativedelta(months=1)
    test_date = processed_date
    train_filename = f"{dataset}_tripdata_{train_date.year - 1}-{str(train_date.month).zfill(2)}.parquet"
    val_filename = f"{dataset}_tripdata_{val_date.year - 1}-{str(val_date.month).zfill(2)}.parquet"
    test_filename = f"{dataset}_tripdata_{test_date.year - 1}-{str(test_date.month).zfill(2)}.parquet"
    return train_filename, val_filename, test_filename

@flow()
def main(date=None):
    train_filename, val_filename, test_filename = get_paths(date=date, dataset='green').result()
    download_dataset_by_date(RAW_DATA_PATH, train_filename, wait_for=[get_paths])
    download_dataset_by_date(RAW_DATA_PATH, val_filename, wait_for=[get_paths])
    download_dataset_by_date(RAW_DATA_PATH, test_filename, wait_for=[get_paths])
    train_path = os.path.join(RAW_DATA_PATH, train_filename)
    val_path = os.path.join(RAW_DATA_PATH, val_filename)
    test_path = os.path.join(RAW_DATA_PATH, test_filename)
    dv, rf = train(train_path, val_path, test_path, DEST_PATH, date).result()

# main()

# test function
date = '2022-07-17'
main(date)
