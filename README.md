# DPA-Chicago-VLIN ✒️

Repositorio para la clase de Arquitectura de Producto de Datos, primavera 2021-ITAM

- _Arenas Morales Nayeli_
- _Hernández Martínez Luz Aurora_
- _Sánchez Gutiérrez Vianney_
- _Santiago Castillejos Ita Andehui_

# Summary de los datos: 📋

Datos: 
- [**Chicago Food Inspections**](https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5)

Al 15 de enero de 2021 a las 7:39 p.m.
  - Número de registros: 215,067
  - Número de columnas: 17
  - Qué variables son, qué información tiene:

    - **Inspection ID**: Identificador consecutivo de tipo numérico.

    - **DBA Name**: Acrónimo de 'Doing business as', que es el nombre legal del establecimiento, de tipo texto.

    - **AKA Name**: Acrónimo de 'Also known as' el nombre por el que es conocido el establecimiento, de tipo texto.

    - **License #**: Número de licencia asignado por el 'Department of Business Affairs and Consumer Protection', de tipo numérico.

    - **Facility Type**: Tipo de servicio según su descripción: bakery, banquet hall, candy store, caterer, coffee shop, day care center (for ages less than 2), day care center (for ages 2 – 6), day care center (combo, for ages less than 2 and 2 – 6 combined), gas station, Golden Diner, grocery store, hospital, long term care center(nursing home), liquor store, mobile food dispenser, restaurant, paleteria, school, shelter, tavern, social club, wholesaler, or Wrigley Field Rooftop. Tipo texto.
    
    - **Risk**: Cada establecimiento se categoriza según el tipo de riesgo a la salud, esto es 1 el más alto a 3 el más bajo. Tipo texto.
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
    
  - Pregunta analítica: ¿El establecimiento pasará o no la inspección?
  - Frecuencia de actualización de los datos: Diaria, aunque para efectos del proyecto serà de manera semanal.
  

# Reproducibilidad.

**Nota:** Recordar que todo esto tiene que ser ejecutado desde tu ambiente de trabajo seleccionado, ejecutando `pyenv activate <<tu_ambiente>>`

El notebook `Chicago_food_inspections.ipynb` con el Análisis exploratorio se encuentra en la carpeta `notebooks/eda/`.

Para este notebook utilizamos **Python 3.7.4**
1. En la carpeta data, colocar el archivo `Food_Inspections.csv` que està disponible en este [**Drive**](https://drive.google.com/file/d/1Pyobds5_o_4wKHbZQTsmzfVd-NszjEQM/view?usp=sharing) 
2. En tu ambiente virtual hay que instalar los requirements.txt : `pip install -r requirements.txt`
3. Hay que colocarnos en la carpeta del repositorio.
-----

# Ingestión y almacenamiento automatizado

**Nota:** Para este punto, cabe mencionar que el archivo `requirements.txt` ya fue actualizado para que este contenga las librerìas `boto3, PyYAML, pickle y sodapy`.

1. Para este checkpoint se espera que se tenga un archivo que se encuentra en tu carpeta `conf/local/` con las credenciales de aws, este archivo deberá ser llamado `credentials.yaml` con el siguiente formato:

```
s3:
  aws_access_key_id : "xxxxxx"
  aws_secret_access_key : "xxxxxx"
food_inspections:
  api_token: "xxxxxxx"
```

Donde las llaves de `s3` son para interactuar de manera más sencilla con el servicio de almacenamiento de archivos de `aws`.
El apartado de `food_inspections` contiene en la llave `api_token` que es el token generado desde [**aqui**](https://data.cityofchicago.org/login?return_to=%2Fprofile%2Fedit%2Fdeveloper_settings). Para más informaciòn se puede consultar [**aqui**](https://dev.socrata.com/foundry/data.cityofchicago.org/4ijn-s7e5).


2. También se espera que dentro de _aws_ se tenga un bucket llamado `data-product-architecture-equipo-8`.

3. Los pasos para el proceso de ingestión son los siguientes:
    
    a. En tu terminal escribe `ipython3`

    b. Importa las funciones creadas para la ingestión y alamcenamiento:

                ```
                from src.utils.general import * 

                from src.pipeline.ingesta_almacenamiento import *

                ```
    
    c. Es importante ejecutar los siguientes comandos en este orden:

                ```
                inicial = ingesta_inicial(get_client(),300000)

                guardar_ingesta(inicial, 'data-product-architecture-equipo-8','ingestion/initial/historic-inspections-')

                consecutiva = ingesta_consecutiva(get_client(),"2021-02-18T00:00:00.000",1000, delta=False)

                guardar_ingesta(consecutiva,'data-product-architecture-equipo-8','ingestion/consecutive/consecutive-inspections-')

                ```

        **Nota:** Especificaciones sobre la función `ingesta_consecutiva`: el parámetro _"fecha"_ se usa si se quiere descargar en una fecha específica, dejando la variable _"delta"_ en `False`. Si, como es el objetivo de este proyecto, se desea descargar la información en intervalos de tiempo iguales (7 días por ejemplo) se usa el parámetro _"delta"_ igual a `True`. 

    d. Revisa dentro de tu bucket de aws que la información esté almacenada.

# Bastión

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
│
├── data               <- Space for data
├── docs               <- Space for Sphinx documentation
│
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
    ├── utils      <- Functions used across the project
    │
    │
    ├── etl       <- Scripts to transform data from raw to intermediate
    │
    │
    ├── pipeline
```
