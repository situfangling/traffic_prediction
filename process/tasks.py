# coding=utf-8

import os
from celery import shared_task
from process.data_process import process
from traffic_prediction.settings import BASE_DIR

@shared_task
def process_data():
    path_pkl_file = os.path.join(BASE_DIR, "data/boundary.pkl").replace('\\', '/')  ##这里data前面不用加斜杠
    print(path_pkl_file)
    process(path_pkl_file)