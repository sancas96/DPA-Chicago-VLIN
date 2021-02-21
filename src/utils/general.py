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


