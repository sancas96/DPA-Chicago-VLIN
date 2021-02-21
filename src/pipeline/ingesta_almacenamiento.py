from datetime import date, timedelta
import pandas as pd
from sodapy import Socrata
import yaml

from src.utils.general import get_s3_client


def get_client():
    url, api_token, username, password = get_city_chicago_credentials()
    return Socrata(url, api_token, username, password)


def get_city_chicago_credentials():
    """ load yaml cofigurations """
    with open("conf/local/credentials.yaml", 'r') as f:
        config = yaml.safe_load(f)

    food_inspections = config["food_inspections"]
    url = food_inspections["dataset_domain"]
    username = food_inspections["username"]
    password = food_inspections["password"]
    api_token = food_inspections["api_token"]

    return url, api_token, username, password


def ingesta_inicial():
    dataset_id = "4ijn-s7e5"
    client = get_client()
    results = client.get_all(dataset_id)
    results_df = pd.DataFrame.from_records(results)
    filename = f"historic-inspections-{date.today()}.pkl"
    results_df.to_pickle(filename)
    return filename


def ingesta_consecutiva():
    dataset_id = "4ijn-s7e5"
    client = get_client()
    today = date.today()
    delta_date = today - timedelta(days=7)
    where = f"inspection_date>='{delta_date}'"
    results = client.get(dataset_id, where=where)
    results_df = pd.DataFrame.from_records(results)
    filename = f"consecutive-inspections-{today}.pkl"
    results_df.to_pickle(filename)
    return filename


def upload_info_s3(initial_data = False):
    client = get_s3_client()
    if initial_data:
        filename = ingesta_inicial()
        s3_key = f"ingestion/initial/{filename}"
    else:
        filename = ingesta_consecutiva()
        s3_key = f"ingestion/consecutive/{filename}"
    client.upload_file(filename,"data-product-architecture-equipo-8",s3_key)