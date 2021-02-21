import yaml

def read_yaml(credentials_file):
    """ load yaml cofigurations """
    config = None
    try: 
        with open (credentials_file, 'r') as f:
            config = yaml.safe_load(f)
    except:
        raise FileNotFoundError('Couldnt load the file')
    return config

def get_s3_credentials(credentials_file):
    s3_credentials=read_yaml(credentials_file)['s3']
    return s3_credentials

def get_api_token(credentials_file):
    token=read_yaml(credentials_file)['food_inspections']
    return token


'''
#Código Ita 

import yaml
import boto3


def get_s3_client():
    """ load yaml cofigurations """
    with open("conf/local/credentials.yaml", 'r') as f:
        config = yaml.safe_load(f)

    s3 = config["s3"]
    aws_access_key_id = s3["aws_access_key_id"]
    aws_secret_access_key = s3["aws_secret_access_key"]
    client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    return client
'''