# DPA-Chicago-VLIN ✒️

Repositorio para la clase de Arquitectura de Producto de Datos, primavera 2021-ITAM

| Nombre | usuario git |
|-------|-----------------|
|Arenas Morales Nayeli | arenitss |
|Hernández Martínez Luz Aurora | LuzVerde23 |
|Sánchez Gutiérrez Vianney |visagu55 |
|Santiago Castillejos Ita Andehui | sancas96 |

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

**Importante** Recordar que todo el proyecto debe ser ejecutado desde tu ambiente de trabajo seleccionado, ejecutando `pyenv activate <<tu_ambiente>>`

Para este proyecto utilizamos la versioń **Python 3.7.4**
1. En la carpeta data, colocar el archivo `Food_Inspections.csv` que está disponible en este [**Drive**](https://drive.google.com/file/d/1Pyobds5_o_4wKHbZQTsmzfVd-NszjEQM/view?usp=sharing)
2. En tu ambiente virtual hay que instalar las librerías del archivo requirements.txt : `pip install -r requirements.txt`
3. En la terminal debemos estar ubicados en la carpeta de este repositorio y ejecutar un `export PYTHONPATH=$PWD`
-----

# Análisis Exploratorio ⌨️
El notebook `Chicago_food_inspections.ipynb` con el análisis exploratorio se encuentra en la carpeta `notebooks/eda/`.

# Ingestión y almacenamiento automatizado con Luigi 🛠️

**Nota:** Para la correcta ejecución de la ingestión y almacenamiento se actualizó el archivo `requirements.txt`.

1. Para la ejecución de este checkpoint se asume que se tiene un archivo que se encuentra en la carpeta `conf/local/` con las credenciales de aws, este archivo deberá ser llamado `credentials.yaml` con el siguiente esqueleto:

```
s3:
  aws_access_key_id : "xxxxxx"
  aws_secret_access_key : "xxxxxx"
food_inspections:
  api_token: "xxxxxxx"
```

Donde las llaves de `s3` son para interactuar de manera más sencilla con el servicio de almacenamiento de archivos de `aws`.
El apartado de `food_inspections` contiene la llave `api_token` que es el token generado desde [**aquí**](https://data.cityofchicago.org/login?return_to=%2Fprofile%2Fedit%2Fdeveloper_settings) que funcionará para hacer la ingestión de la API. Para más información se puede consultar [**aquí**](https://dev.socrata.com/foundry/data.cityofchicago.org/4ijn-s7e5).

2. De igual manera se asume que dentro de _aws_ se tenga levantado un bucket llamado `data-product-architecture-equipo-8` con la siguiente estructura:
```
    ├── data-product-architecture-equipo-8
    │   ├── ingesta    
```
3. Ejecutar `luigid` y en el navegador entrar a `http://localhost:8082/static/visualiser/index.html`

4. Para la ingesta y almacenamiento ocuparemos como orquestador a [Luigi](https://luigi.readthedocs.io/en/stable/index.html). Tanto para la ingesta y almacenamiento, los parámetros para las tareas son los siguientes:

    - **tipo_ingesta**: historica o consecutiva.
    - **fecha**: Fecha en la que se está haciendo la ingesta con respecto a inspection date.
    - **bucket**: nombre de tu bucket en `aws`.


La estructura desarrollada es la siguiente:

  Ingesta inicial: Con las credenciales que se dieron de alta para conectarnos a la API de _data.cityofchicago.org_, descargamos la base de datos disponible hasta la fecha. Este archivo se guardara con el nombre `historica-{fecha}.pkl`
```
PYTHONPATH=$PWD luigi --module src.pipeline.almacenamiento almacenar --tipo-ingesta historica --fecha 2021-01-21T00:00:00.00 --bucket data-product-architecture-equipo-8
```    
  Ingesta consecutiva: Es la descarga de los datos posteriores a la ingesta inicial hasta la fecha solicitada. Este archivo se guardara con el nombre `consecutiva-{fecha}.pkl`
```
PYTHONPATH=$PWD luigi --module src.pipeline.almacenamiento almacenar --tipo-ingesta consecutiva --fecha 2021-03-17T00:00:00.00 --bucket data-product-architecture-equipo-8
```

5. Revisa dentro de tu bucket de aws que la información esté almacenada.

Al terminar este proceso verificamos el DAG en Luigi.

<img width="1020" alt="imagen" src="https://github.com/sancas96/DPA-Chicago-VLIN/blob/main/images/dag_luigi.png">


# Bastión 📖

Para tener acceso al Bastión se requiere que el administrador le haya dado acceso al mismo y tener un usuario asignado y correr en su terminal lo siguiente:

    `ssh -i <<llave_privada>> <<usuario>>@ip_del_ec2`

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
