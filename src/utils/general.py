import yaml
import psycopg2

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

def get_database_connection (credentials_file):
    """
        Esta función recibe como parámetro:
            credentials_file: archivo generado por read_yaml donde están nuestras credenciales.

        Y regresa los parámetros para conectarse a la base de postgres:
            user, password, database, host, port
        """
    database_params=read_yaml(credentials_file)['chicago_database']
    return database_params

def query_database (consulta):
    """
        Esta función hace una consulta a la base de datos postgres y recibe como parámetro:
            consulta: el texto de la consulta entre comillas y con punto y coma.

        Y regresa:
            Un objeto de lista con el resultado de la consulta ejecutada.
        """
    # Conectar a base de datos
    db_creds = get_database_connection('conf/local/credentials.yaml')
    conn = psycopg2.connect(f"dbname={db_creds['database']} user={db_creds['user']} password={db_creds['password']} host={db_creds['host']} port={db_creds['port']}")
    cur = conn.cursor()
    cur.execute(consulta)
    resultado_consulta=list(cur.fetchall())
    cur.close()
    conn.close()
    return resultado_consulta

def get_db_conn_sql(credentials_file):

    """
    :param credentials_file:
    :return: conection
    """

    db_creds = get_database_connection('../../conf/local/credentials.yaml')
    db_conn_str = f"postgresql://{db_creds['user']}:{db_creds['password']}@{db_creds['host']}:{db_creds['port']}/{db_creds['database']}"
    return db_conn_str
    

    
    





