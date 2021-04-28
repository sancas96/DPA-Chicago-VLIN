# DPA-Chicago-VLIN ✒️

Repositorio para la clase de Arquitectura de Producto de Datos, primavera 2021-ITAM

| Nombre | usuario git |
|-------|-----------------|
|Arenas Morales Nayeli | arenitss |
|Hernández Martínez Luz Aurora | LuzVerde23 |
|Santiago Castillejos Ita Andehui | sancas96 |
|Sánchez Gutiérrez Vianney | visagu55 |

# Summary de los datos: 📋

Datos:
- [**Chicago Food Inspections**](https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5)

Al 15 de enero de 2021 a las 7:39 p.m.
  - Número de registros: 215,067
  - Número de columnas: 17
  - Qué variables son, qué información tiene:

    - **Inspection ID**: Identificador consecutivo. Tipo numérico.
    - **DBA Name**: Acrónimo de 'Doing business as', que es el nombre legal del establecimiento. Tipo texto.
    - **AKA Name**: Acrónimo de 'Also known as' el nombre por el que es conocido el establecimiento. Tipo texto.
    - **License #**: Número de licencia asignada por el 'Department of Business Affairs and Consumer Protection'. Tipo numérico.
    - **Facility Type**: Tipo de servicio según su descripción: bakery, banquet hall, candy store, caterer, coffee shop, day care center (for ages less than 2), day care center (for ages 2 – 6), day care center (combo, for ages less than 2 and 2 – 6 combined), gas station, Golden Diner, grocery store, hospital, long term care center(nursing home), liquor store, mobile food dispenser, restaurant, paleteria, school, shelter, tavern, social club, wholesaler, or Wrigley Field Rooftop. Tipo texto.
    - **Risk**: Cada establecimiento se categoriza según el tipo de riesgo a la salud, esto es 1 (el más alto) a 3 (el más bajo). Tipo texto.
    - **Address**: Dirección para facilitar su ubicación. Tipo texto.
    - **City**: Ciudad. Tipo texto.
    - **State**: Estado. Tipo texto.
    - **Zip**: Código postal. Tipo numérico.
    - **Inspection Date**: Describe la fecha en que la inspección ocurrió, un establecimiento puede tener múltiples inspecciones. Tipo de fecha y hora.
    - **Inspection Type**: Las inspecciones se pueden describir como sigue:
        * canvass: el tipo más común de inspección que se ejecuta con una frecuencia relativa al riesgo del establecimiento.
        * consultation: cuando la inspección se realiza a petición del dueño previo a la apertura del establecimiento.
        * complaint: cuando la inspección se realiza en respuesta a una queja en contra del establecimiento.
        * license: cuando la inspección se realiza como un requerimiento para que el establecimiento pueda recibir su licencia para operar.
        * suspect food poisoning: inspección que se realiza en respuesta a una o más personas que indican haberse enfermado como resultado de haber comido en el establecimiento.
        * task-force inspection: cuando la inspección de un bar o taberna se ejecuta. Tipo texto.

      La re-inspección puede ocurrir para todos los tipos de inspecciones y se nombrarían de la misma manera.
    - **Results**: Muestra el resultado de la inspección bajo las siguientes categorías: puede aprobarse, aprobarse con condiciones o fallar. Se encontró que "pasar" no tenía violaciones críticas o graves (violación número 1-14 y 15-29, respectivamente).Las categorias pueden ser: 'pass', 'pass with conditions' y 'fail'.  Tipo texto.
    - **Violations**: Un establecimiento puede recibir uno o más de 45 (1-44 y 70) infracciones distintas a la norma. Además se enuncia el requisito que el establecimiento debe cumplir para NO recibir una infracción, seguido de una descripción específica de los hallazgos que causaron la violación. Tipo texto.
    - **Latitude**: Latitud del establecimiento. Tipo numérico.
    - **Longitude**: longitud del establecimiento. Tipo numérico.
    - **Location**: la latitud y longitud del establecimiento. Tipo localización.

  - La pregunta analítica que queremos resolver es: ¿El establecimiento pasará o no la inspección?
  - Frecuencia de actualización de los datos: Diaria, aunque para efectos del proyecto será de manera semanal.


# Reproducibilidad y requerimientos. ⚙️

**Importante** Este proyecto debe ser ejecutado desde el ambiente de trabajo seleccionado, ejecutando `pyenv activate <<tu_ambiente>>`.

Para la infraestructura de este proyecto ocupamos la siguiente arquitectura:

| **Bastión** | **EC2 de procesamiento** | **RDS** |
|-------|-------| -------|
| Ubuntu Server 18.04| Ubuntu Server 18.04| PostgreSQL 12.5-R1 |
| 64 bits (x86) | 64 bits (x86) |
| t2.micro | t2.medium | db.t2.micro  |
| Volumen 20 GiB | Volumen 80 GiB |

Las cuales se iran ocupando a lo largo de esta lectura.

Para este proyecto utilizamos la versioń **Python 3.7.4**
1. Para la reproducibilidad del análisis exploratorio de datos: en la carpeta data, colocar el archivo `Food_Inspections.csv` que está disponible en este [**Drive**](https://drive.google.com/file/d/1Pyobds5_o_4wKHbZQTsmzfVd-NszjEQM/view?usp=sharing)
2. Para la reproducibilidad de los _tasks_ se creo  la infraestructura en AWS ya mencionada, a la cual tendremos acceso con :

#### Bastión 📖

  Para tener acceso a cualquiera de estos (Bastión, EC2 y RDS) se requiere que el administrador les haya dado acceso a los mismos y tener un usuario asignado. Con lo anterior ya cumplido, hay que correr en su terminal lo siguiente:

```
    ssh -o ServerAliveInterval=60 -i ~/.ssh/<<llave_privada>> <<tu_usuario>>@ip_del_ec2
```

#### EC2 🔧

  Aquí es donde se encuentra toda la estructura de este repositorio.

```
    ssh -o ServerAliveInterval=60 -i ~/.ssh/<<llave_privada>> <<tu_usuario>>@ip_del_ec2
```
#### rds 📦

  _Framework_ con los metadatas de almacenamiento y procesamiento

```
    psql -U chicago_food -h chicago-food-2021.ctd292l1zdjq.us-west-2.rds.amazonaws.com -d chicago_food
```

3. En el ambiente virtual hay que instalar las librerías del archivo requirements.txt que se encuentra dentro de este repositorio: `pip install -r requirements.txt`
4. En la terminal debemos estar ubicados en la carpeta de este repositorio y ejecutar un `export PYTHONPATH=$PWD`

5. Para poder tener el mismo esqueleto de la base de datos en postgress se debe crear un usuario y después crear la base de datos y darle los permisos correspondientes:
```
  sudo -u postgres createuser --login --pwprompt chicago_food
  create database chicago_food;
  sudo -u postgres createdb --owner=chicago_user chicago_food
```
Después de este paso es necesario crear los esquemas como se sugiere en el `script`  que está en la ruta `sql`.

6. La carpeta `conf/local/` debe contener las credenciales para la conexión tanto al _bucket_ en aws (s3), el _token_ para obtener la información de la base de datos a la que nos estamos conectando (food_inspections) y las credenciales para la conexión a la base de datos relacional donde se guardará nuestra información.

+ Las llaves de `s3` son para interactuar de manera más sencilla con el servicio de almacenamiento de archivos de `aws`.

+ El apartado de `food_inspections` debe contener la llave `api_token` que es el token generado desde [**aquí**](https://data.cityofchicago.org/login?return_to=%2Fprofile%2Fedit%2Fdeveloper_settings) que funcionará para hacer la ingestión de la API. Para más información se puede consultar [**aquí**](https://dev.socrata.com/foundry/data.cityofchicago.org/4ijn-s7e5).

+ Asimismo, la carpeta debe contener las credenciales para ingresar a la base de datos (RDS).

Este archivo deberá ser llamado `credentials.yaml` con el siguiente esqueleto.

```
s3:
  aws_access_key_id : "xxxxxx"
  aws_secret_access_key : "xxxxxx"
food_inspections:
  api_token: "xxxxxxx"
chicago_database:
  user: "chicago_food"
  password: "xxxxxxx"
  database: "chicago_food"
  host: "chicago-food-2021.ctd292l1zdjq.us-west-2.rds.amazonaws.com"
  port: "5432"
```

<img width="1020" alt="imagen" src="https://github.com/sancas96/DPA-Chicago-VLIN/blob/main/images/ec2_security_groups.png">

Tomado de [data-product-architecture](https://github.com/ITAM-DS/data-product-architecture)

-----

# Análisis Exploratorio ⌨️
El notebook `Chicago_food_inspections.ipynb` con el análisis exploratorio se encuentra en la carpeta `notebooks/eda/`. Para este análisis se uso como información de corte el archivo .csv mencionado en el punto 1 del inciso anterior.

# Luigi 🛠️
## Ingesta y almacenamiento

1. Se asume que dentro de _aws_ se tenga levantado un bucket llamado `data-product-architecture-equipo8` con la siguiente estructura:
```
    ├── data-product-architecture-equipo8
    │   ├── ingesta    
```
2. Para poder visualizar los ejercicios en EC2 de procesamiento se realiza un doble espejo que va de:
```
        EC2 de procesamiento -> Bastión -> tu computadora
```
+ En EC2 de procesamiento se ejecuta `luigid`.
+ En bastión realizas el primer _portforwdaring_:
```
ssh -i ~/.ssh/<<llave_privada>> -NL localhost:4444:localhost:8082 <<usuario>>@ip_del_ec2
```
+ En tu computadora realizas el segundo _portforwdaring_:
```
ssh -i ~/.ssh/<<llave_privada>>-NL localhost:4444:localhost:4444 <<usuario>>@ip_del_ec2
```
 En el navegador entras a [http://localhost:4444](http://localhost:4444)

3. Luigi

Para la ingesta, almacenamiento, limpieza, ingeniería de características, entrenamiento y selección del modelo ocuparemos como orquestador a [Luigi](https://luigi.readthedocs.io/en/stable/index.html). Para cada una de estas tareas los parametros necesarios pueden ser los siguientes:

- **tipo_ingesta**: historica o consecutiva.
- **fecha**: Fecha en la que se está haciendo la ingesta con respecto a inspection date.
- **bucket**: nombre de tu bucket en `aws`.
- **tamanio**: tamaño del archivo almacenado.
- **tipo-prueba**: infinito o size

La estructura desarrollada es la siguiente:

  Ingesta inicial y metadata: Con las credenciales que se dieron de alta para conectarnos a la API de _data.cityofchicago.org_, descargamos la base de datos disponible hasta la fecha. Este archivo se guardara con el nombre `historica-{fecha}.pkl`
```
PYTHONPATH="." luigi --module src.pipeline.metadata_almacenamiento metadata_almacenar --tipo-ingesta historica --fecha 2021-03-29T00:00:00.00 --bucket data-product-architecture-equipo8 --tamanio 100
```    
  Ingesta consecutiva: Es la descarga de los datos posteriores a la ingesta inicial hasta la fecha solicitada. Este archivo se guardara con el nombre `consecutiva-{fecha}.pkl`
```
PYTHONPATH="." luigi --module src.pipeline.metadata_almacenamiento metadata_almacenar --tipo-ingesta consecutiva --fecha 2021-04-05T00:00:00.00 --bucket data-product-architecture-equipo8 --tamanio 100
```
Cada uno de estos ejemplos almacena también la _metadata_ de cada uno de los procesos, esto es en la tabla de _rds_ `metadata_ingesta` y `metadata_almacenar`.

# Limpieza de datos
Con la base de datos obtenida en las tareas de ingestión y almacenamiento, hacemos un proceso de limpieza donde:

  - Se eliminan los datos nulos de las variables `inspection_date`, `license_`, `latitude`, `longitude`,
  - Se eligen solo los establecimientos que están en operación,
  - Se eliminan los duplicados,
  - Se sustituyen los datos nulos restantes con cero.

Metadata de limpieza de datos: Guardamos la metadata generada por el proceso de limpieza. Este es un ejemplo de cómo correrlo
```
PYTHONPATH="." luigi --module src.pipeline.metadata_limpieza metadata_limpiar --tipo-ingesta consecutiva --fecha 2021-04-12T00:00:00.00 --bucket data-product-architecture-equipo8 --tamanio 100 --tipo-prueba infinito
```
Este proceso genera las tablas `data.limpieza`, `data.metadata_limpieza` que contiene la tabla con esta limpieza y la _metadata_ de la misma, respectivamente.

# Ingeniería de características
Con los datos limpios, corremos el proceso de ingeniería de características en donde:
  - Convertimos la variable de infracciones en columnas de tipo dummy,
  - Aplicamos label encoding (convertir a categorías numéricas variables categóricas de tipo string),
  - Eliminamos las variables que no aportan información relevante al modelo.

Metadata de ingeniería de características: Guardamos la metadata generada por el proceso de ingeniería de características.
```
PYTHONPATH="." luigi --module src.pipeline.metadata_ingenieria_caract metadata_ingenieria --tipo-ingesta consecutiva --fecha 2021-04-15T00:00:00.00 --bucket data-product-architecture-equipo8 --tamanio 100 --tipo-prueba infinito
```
Este proceso genera las tablas `data.ingenieria`, `data.metadata_ingenieria` que contiene la tabla con esta ingeniería de características y la _metadata_ de la misma, respectivamente.

# Entrenamiento
Con el dataset listo, se divide en entrenamiento y prueba, con porcentajes del 75% y 25% respectivamente. Se corren los siguientes tres modelos de clasificación haciendo uso de la librería _scikit learn_:
  - XGboost,
  - KNN,
  - Logistic Regression.

De estos tres calculamos el _accuracy_ y guardamos cada modelo y sus parámetros en archivos pkl.

Metadata de entrenamiento de modelos: Guardamos la metadata generada por el proceso de entrenamiento.
```
PYTHONPATH="." luigi --module src.pipeline.metadata_entrenamiento metadata_entrenar --tipo-ingesta consecutiva --fecha 2021-04-23T00:00:00.00 --bucket data-product-architecture-equipo8 --tamanio 100 --tipo-prueba infinito

PYTHONPATH="." luigi --module src.pipeline.test_entrenamiento test_entrenar --tipo-ingesta consecutiva --fecha 2021-04-23T00:00:00.00 --bucket data-product-architecture-equipo8 --tamanio 1000000000 --tipo-prueba infinito
```

# Selección de modelo
En esta parte se pretende tomar el modelo con el mejor _accuracy_, así que elegimos el máximo _accuracy_ de los 3 modelos de entrenamiento.

Metadata de selección del modelo: Guardamos la metadata generada por el proceso de selección del modelo.
```
PYTHONPATH="." luigi --module src.pipeline.metadata_seleccion metadata_seleccionar --tipo-ingesta consecutiva --fecha 2021-04-23T00:00:00.00 --bucket data-product-architecture-equipo8 --tamanio 100 --tipo-prueba infinito

PYTHONPATH="." luigi --module src.pipeline.metadata_seleccion metadata_seleccionar --tipo-ingesta consecutiva --fecha 2021-04-23T00:00:00.00 --bucket data-product-architecture-equipo8 --tamanio 100 --tipo-prueba shape
```

Si las sentencias anteriores se corren en el orden indicado, podremos ver un _DAG_ de Luigi similar a este:

<img width="1020" alt="imagen" src="https://github.com/sancas96/DPA-Chicago-VLIN/blob/main/images/luigi_checkpoint4.png">

# Nota:
Este producto de datos continúa en desarrollo, por lo que aún faltan algunas mejoras,recomendaciones o mejores prácticas que se estarán atendiendo:
- Las sentencias que se corren de luigi idealmente no deberían contener en la fecha el formato de tiempo.
- Igualmente en la sentencia de luigi lo ideal sería no introducir un parámetro para el nombre del _bucket_ e incluirlo como parte de una constante en el archivo `constants.py`.


**Nota:** El usuario lmillan ya fue asignado con la llave correspondiente.

---

**Figura 1**. Estructura básica del proyecto.

```  
├── README.md          <- The top-level README for developers using this project.
├── conf
│   ├── base           <- Space for shared configurations like parameters
│   └── local          <- Space for local configurations, usually credentials
├── data               <- Space for data
├── docs               <- Space for Sphinx documentation
├── images             <- Space for images
├── notebooks          <- Jupyter notebooks.
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── results            <- Intermediate analysis as HTML, PDF, LaTeX, etc.
│
├── requirements.txt   <- The requirements file
│
├── .gitignore         <- Avoids uploading data, credentials, outputs, system files etc
│
├── infrastructure
├── sql
├── setup.py
└── src                <- Source code for use in this project.
    ├── __init__.py    <- Makes src a Python module
    │
    ├── utils          <- Functions used across the project
    │
    │
    ├── etl            <- Scripts to transform data from raw to intermediate
    │
    │
    └── pipeline       <- Scripts to data ingestion
```
