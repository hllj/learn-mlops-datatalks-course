import os
from urllib import request
from datetime import datetime
from prefect import task

@task
def download_dataset_by_date(dataset_folder, dataset_filename):
    try:
        data_path = os.path.join(dataset_folder, dataset_filename)
        if os.path.exists(data_path) is False:
            request.urlretrieve(
                f"https://d37ci6vzurychx.cloudfront.net/trip-data/{dataset_filename}", 
                data_path
            )
    except:
        raise Exception('Can not download dataset')
