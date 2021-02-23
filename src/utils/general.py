import yaml

def read_yaml(credentials_file):
    """
    Descarga yaml para importar las credenciales.
    """
    config = None
    try: 
        with open (credentials_file, 'r') as f:
            config = yaml.safe_load(f)
    except:
        raise FileNotFoundError('Could not load the file')
    return config


def get_s3_credentials(credentials_file):
    """
    Esta función recibe como parámetro:
        credentials_file: archivo generado por read_yaml.

    Y regresa:
        s3_credential: las credenciales para comunicarse con AWS.
    """
    s3_credentials=read_yaml(credentials_file)['s3']
    return s3_credentials


def get_api_token(credentials_file):
    """
        Esta función recibe como parámetro:
            credentials_file: archivo generado por read_yaml.

        Y regresa:
            token: el token para comunicarse con la API.
        """
    token=read_yaml(credentials_file)['food_inspections']
    return token