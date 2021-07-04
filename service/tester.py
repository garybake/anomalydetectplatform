"""Generate test requests for prediction service"""

import csv
import json
import random
from typing import List

import requests

SOURCE_DATA = '../jupyter/test.csv'
BASE_URL = 'http://localhost:8000'

def get_data(max_records:int=20) -> List[List[float]]:
    with open(SOURCE_DATA) as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)
        data = list(reader)

    data = data[:max_records]
    data = [[float(x[0]), float(x[1])] for x in data]
    return data


def do_prediction_request(datum: List[str])-> None:
    url = f'{BASE_URL}/prediction'

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    body = {
        "feature_vector": datum,
        "score": random.random() <= 0.25
    }
    

    resp = requests.post(url, data=json.dumps(body), headers=headers)

    if resp.status_code != 200:
        print(resp.status_code)
   


def do_info_request():
    url = f'{BASE_URL}/model_information'
    resp = requests.get(url)
    print(f'Info request: {resp.status_code}')


def run_dataset(data: List[List[float]]) -> None:
    requests_done = 0
    for datum in data:
        do_prediction_request(datum)

        requests_done += 1
        if requests_done % 10 == 0:
            print(f'Done {requests_done} records')
    do_info_request()
    

def main()-> None:
    data = get_data(max_records=1000000)
    print(f'{len(data)} rows found')
    run_dataset(data)


if __name__ == "__main__":
    main()