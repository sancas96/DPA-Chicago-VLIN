# DPA-Chicago-VLIN ✒️

Repositorio para la clase de Arquitectura de Producto de Datos, primavera 2021-ITAM

| Nombre | usuario git |
|-------|-----------------|
|Arenas Morales Nayeli | arenitss |
|Hernández Martínez Luz Aurora | LuzVerde23 |
|Santiago Castillejos Ita Andehui | sancas96 |
|Sánchez Gutiérrez Vianney | visagu55 |

# Resumen de los datos: 📋

Datos:
- [**Chicago Food Inspections**](https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5)

Al 15 de enero de 2021 a las 7:39 p.m.
  - Número de registros: 215,067
  - Número de columnas: 17
  - La descripción de cada uno de los campos es la siguiente:

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

  - Para este producto de datos la pregunta analítica que queremos resolver es: ¿El establecimiento pasará o no la inspección?
  - Frecuencia de actualización de los datos: Diaria, aunque para efectos de este proyecto la hacemos de manera semanal.


# Reproducibilidad y requerimientos. ⚙️

**Importante** Este proyecto debe ser ejecutado desde el ambiente de trabajo seleccionado, ejecutando `pyenv activate <<tu_ambiente>>`.

# Infraestructura

Para la infraestructura de este proyecto ocupamos la siguiente arquitectura:

| **Bastión** | **EC2 de procesamiento** | **RDS** |
|-------|-------| -------|
| Ubuntu Server 18.04| Ubuntu Server 18.04| PostgreSQL 12.5-R1 |
| 64 bits (x86) | 64 bits (x86) |
| t2.micro | t2.medium | db.t2.micro  |
| Volumen 20 GiB | Volumen 80 GiB |

Las cuales se irán ocupando a lo largo de esta lectura.

Para este proyecto utilizamos la versioń **Python 3.7.4**
1. Para la reproducibilidad del análisis exploratorio de datos: en la carpeta data, colocar el archivo `Food_Inspections.csv` que está disponible en este [**Drive**](https://drive.google.com/file/d/1Pyobds5_o_4wKHbZQTsmzfVd-NszjEQM/view?usp=sharing)
2. Para la reproducibilidad de los _tasks_ se creo  la infraestructura en AWS ya mencionada, a la cual tendremos acceso primero a través de:

#### Bastión 📖

  Para tener acceso a cualquiera de estos (Bastión, EC2 y RDS) se requiere que el administrador les haya dado acceso a los servicios y tener un usuario asignado. Con lo anterior ya cumplido, hay que correr en la terminal lo siguiente:

```
    ssh -o ServerAliveInterval=60 -i ~/.ssh/<<llave_privada>> <<tu_usuario>>@ip_del_ec2
```

#### EC2 🔧

  En esta máquina virtual se encuentra toda la estructura de este repositorio.

```
    ssh -o ServerAliveInterval=60 -i ~/.ssh/<<llave_privada>> <<tu_usuario>>@ip_del_ec2
```
#### RDS 📦

  Base de datos que contiene las tablas de limpieza e ingeniería de características incluidos los metadatas de todas las tareas:

```
    psql -U chicago_food -h chicago-food-2021.ctd292l1zdjq.us-west-2.rds.amazonaws.com -d chicago_food
```

3. En el ambiente virtual hay que instalar las librerías de python del archivo requirements.txt que se encuentra dentro de este repositorio: `pip install -r requirements.txt`
4. En la terminal debemos estar ubicados en la carpeta de este repositorio y ejecutar un `export PYTHONPATH=$PWD`

5. Para poder tener el mismo esqueleto de la base de datos en postgress se debe crear un usuario y después crear la base de datos y darle los permisos correspondientes:
```
  sudo -u postgres createuser --login --pwprompt chicago_food
  create database chicago_food;
  sudo -u postgres createdb --owner=chicago_user chicago_food
```
Después de este paso es necesario crear los esquemas como se indica en el `script`  que está en la ruta `sql`. Las tablas que se van creando dentro de la base de datos se generan automáticamente corriendo las tareas de luigi.

6. La carpeta `conf/local/` debe contener las credenciales para la conexión tanto al _bucket_ en aws (s3), el _token_ para obtener la información de la base de datos a la que nos estamos conectando (food_inspections) y las credenciales para la conexión a la base de datos relacional donde se guardará nuestra información.

+ Las llaves de `s3` son para interactuar de manera programática con el servicio de almacenamiento de archivos de `aws`.

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
+ Esta es la arquitectura de la infraestructura usada en este producto de datos:
<img width="1020" alt="imagen" src="https://github.com/sancas96/DPA-Chicago-VLIN/blob/main/images/ec2_security_groups.png">

Referencia: [data-product-architecture](https://github.com/ITAM-DS/data-product-architecture)

-----

# Análisis Exploratorio ⌨️
El notebook `Chicago_food_inspections.ipynb` con el análisis exploratorio se encuentra en la carpeta `notebooks/eda/`. Para este análisis se usó como información de corte el archivo .csv mencionado en el punto 1 del inciso anterior.

# Luigi como Orquestador del producto de datos 🛠️
## Supuestos

1. Se asume que dentro de _aws_ se tenga levantado un bucket llamado `data-product-architecture-equipo8` con la siguiente estructura:
```
    ├── data-product-architecture-equipo8
    │   ├── ingesta
    |   ├── entrenamiento
    |   ├── seleccion
```
2. Para poder visualizar el producto de datos, elaborado en la EC2 de procesamiento, en el navegador de tu computadora se realiza un (_portforwarding_). Para esto se requiere seguir los siguientes pasos:

+ Habilitar en las reglas de entrada de la EC2 de procesamento al puerto 8082 para `luigid`, al 1234 para `Flask` y al 4321 para `Dash`
+ En EC2 de procesamiento se ejecuta `luigid`
+ En EC2 de procesamiento se ejecuta `Flask` ejecutando primero `export FLASK_APP=flask_api.py` y después `flask run --host=0.0.0.0 --port=1234`

+ Antes de ejecutar `Dash` en el script app.py es importante especificar que el host debe ser  el 0.0.0.0. Lo anterior se realiza añadiendo al final:
```
if __name__ == '__main__':
    app.run_server(debug=True, host = ‘0.0.0.0’, port = ‘4321’ )
```
+ En EC2 de procesamiento se ejecuta `Dash`
```
python src/utils/dash_app.py
```
+ En el navegador de tu computadora ejecutas para visualizar `luigid`, `Flask` y `Dash`:
```
ip_del_ec2:8082
ip_del_ec2:4321
ip_del_ec2:1234
```
 
3. Luigi

Para la ingesta, almacenamiento, limpieza, ingeniería de características, entrenamiento, selección, análisis de sesgos e inquidades, predicción, api y monitoreo ocuparemos como orquestador a [Luigi](https://luigi.readthedocs.io/en/stable/index.html). Donde los parámetros los definimos de la siguiente forma:

- **tipo_ingesta**: los parámetros pueden ser "histórica" o "consecutiva".
- **fecha**: Fecha en la que se está haciendo la ingesta con respecto a inspection date, el formato de está fecha es de esta forma: "yyyy-mm-ddT00:00:00.00".
- **bucket**: nombre de tu bucket en `aws`.
- **tamanio**: tamaño del archivo almacenado. Este parámetro sirve para hacer pruebas unitarias sobre los archivos almacenados ya sea localmente o en S3, la prueba identifica si el archivo tiene un número de bits mayor al que se indica en el paŕametro.
- **tipo-prueba**: los parámetros pueden ser "infinito" o "shape". Este parámetro sirve para mostrar el fallo de la prueba unitaria para la tarea de predicción. Lo que valida con "infinito" es que no haya valores infinitos para los campos numéricos y "shape" busca que las tablas de RDS tengan una dimensión de 1.
- **proceso**: puede tomar valores de "entrenamiento" o "prediccion", sirve para identificar en cuál parte del modelo de machine learning nos encontramos.

La estructura de las tareas en luigi es la siguiente:
## Rama 1: Entrenamiento

En esta rama se encuentra todo el proceso para entrenar el modelo con los datos de la base de datos de Chicago.

### Ingesta y almacenamiento

  Ingesta inicial y metadata: Con las credenciales que se dieron de alta para conectarnos a la API de _data.cityofchicago.org_, descargamos la base de datos disponible hasta la fecha. Este archivo se guardará en el bucket S3 en la carpeta _ingesta_ con el nombre `historica-{fecha}.pkl`, la forma de correrlo es la siguiente:
```
PYTHONPATH="." luigi --module src.pipeline.metadata_almacenamiento metadata_almacenar --tipo-ingesta historica --fecha 2021-03-29T00:00:00.00 --bucket data-product-architecture-equipo8 --tamanio 100
```    
  Ingesta consecutiva: Es la descarga de los datos posteriores a la ingesta inicial y hasta la fecha solicitada. Este archivo se guardará con el nombre `consecutiva-{fecha}.pkl` dentro del bucket de S3 en la carpeta de ingesta:
```
PYTHONPATH="." luigi --module src.pipeline.metadata_almacenamiento metadata_almacenar --tipo-ingesta consecutiva --fecha 2021-04-23T00:00:00.00 --bucket data-product-architecture-equipo8 --tamanio 100
```
Cada uno de estos ejemplos almacenan también la _metadata_ de estas tareas, esto es dentro de la base de datos en las tablas `metadata_ingesta` y `metadata_almacenar`, respectivamente. Adicionalmente, en el esquema _test_ crea una tabla llamada _pruebas_unitarias_ donde se almacenan las pruebas unitarias de todas las tareas.

### Limpieza
Con la base de datos obtenida en las tareas de ingestión y almacenamiento, hacemos un proceso de limpieza donde:

  - Se eliminan los datos nulos de las variables `inspection_date`, `license_`, `latitude`, `longitude`,
  - Se eligen solo los establecimientos que están en operación al momento de hacer la inspección del mismo,
  - Se eliminan los duplicados,
  - Se sustituyen los datos nulos restantes con cero.

Metadata de limpieza de datos: Guardamos la metadata generada por el proceso de limpieza en la base de datos con el esquema _metadata_.Este es un ejemplo de cómo debería correrse:
```
PYTHONPATH="." luigi --module src.pipeline.metadata_limpieza metadata_limpiar --tipo-ingesta consecutiva --fecha 2021-04-23T00:00:00.00 --bucket data-product-architecture-equipo8 --tamanio 100
```
Este proceso genera las tablas `data.limpieza`, `metadata.metadata_limpieza` que son las tablas con esta limpieza y la _metadata_ de la misma, respectivamente.

### Ingeniería de características
Con los datos limpios, corremos el proceso de ingeniería de características en donde:
  - Convertimos la variable de infracciones en columnas de tipo dummy,
  - Aplicamos label encoding (convertir a categorías numéricas variables categóricas de tipo string),
  - Eliminamos las variables que no aportan información relevante al modelo.

Metadata de ingeniería de características: Guardamos la metadata generada por el proceso de ingeniería de características. Se corre de esta manera:
```
PYTHONPATH="." luigi --module src.pipeline.metadata_ingenieria_caract metadata_ingenieria --tipo-ingesta consecutiva --fecha 2021-04-23T00:00:00.00 --bucket data-product-architecture-equipo8 --tamanio 100
```
Este proceso genera las tablas `data.ingenieria`, `metadata.metadata_ingenieria` que contiene la tabla con la ingeniería de características y la _metadata_ de la misma, respectivamente.

### Entrenamiento
Con el dataset listo se corren los siguientes tres modelos de clasificación haciendo uso de la librería _scikit learn_:
  - XGboost,
  - KNN,
  - Logistic Regression.

Estos modelos se guardan como formato _.pkl_ en el bucket de S3 en la carpeta de _entrenamiento_.

Metadata de entrenamiento de modelos: Guardamos la metadata generada por el proceso de entrenamiento, esta es la forma de correrlo:
```
PYTHONPATH="." luigi --module src.pipeline.metadata_entrenamiento metadata_entrenar --tipo-ingesta consecutiva --fecha 2021-04-23T00:00:00.00 --bucket data-product-architecture-equipo8 --tamanio 100 --proceso entrenamiento
```

### Selección de modelo
En esta parte se pretende tomar el modelo con el mejor _accuracy_, así que elegimos el máximo _accuracy_ de los 3 modelos de entrenamiento. Esta tarea genera como salida el mejor modelo en el bucket de S3 en la carpeta de _seleccion_.

Metadata de selección del modelo: Guardamos la metadata generada por el proceso de selección del modelo en la tabla _metadata.metadata_seleccion_, aquí ejemplificamos cómo correr esta tarea:
```
PYTHONPATH="." luigi --module src.pipeline.metadata_seleccion metadata_seleccionar --tipo-ingesta consecutiva --fecha 2021-04-23T00:00:00.00 --bucket data-product-architecture-equipo8 --tamanio 100 --proceso entrenamiento
```

### Sesgo e inequidades
Una parte importante del producto de datos es garantizar que nuestro modelo no esté creando inequidades sobre algún segmento específico, por lo que al momento de realizar este modelo, las consideraciones hechas son:
  - Este modelo es un modelo punitivo dado que en caso de que el establecimiento resulte con una calificación negativa entonces podría ser cerrado o clausurado.
  - Se eligió como atributo protegido el _tipo de establecimiento_ ya que nos interesa saber si estamos favoreciendo a un tipo de establecimiento como por ejemplo, los restaurantes.
  - El grupo de referencia para este atributo protegido es el _restaurante_ esto debido a que consideramos que es el segmento que mayormente se da en esta categoaría.
  - Usamos el paquete de [aequitas](http://www.datasciencepublicpolicy.org/projects/aequitas/) para el tratamiento de sesgos e inequidades.
  - Las métricas de cuantificación del sesgo que consideramos fueron: False Positive Rate y False Discovery Rate. La razón del uso de estas métricas es que la primera estará cuantificando de los restaurantes que no pasaron la prueba, ¿cuáles son las posibilidades de que pasaran dado el tipo de establecimiento al que pertenecen? y la segunda métrica estará identificando de aquéllos restaurantes que debieron pasar la inspección, ¿cuáles son las probabilidades de no haber pasado dado el tipo de establecimiento al que pertenencen? 
 
Para ejecutar la tarea de sesgos e inequidad, en conjunto con su prueba unitiaria y la metadata, se correría de la siguiente forma:
```
PYTHONPATH="." luigi --module src.pipeline.metadata_sesgo_ineq metadata_sesg_ineq --tipo-ingesta consecutiva --fecha 2021-04-23T00:00:00.00 --bucket data-product-architecture-equipo8 --tamanio 100 --proceso entrenamiento
```
Esta tarea creará registros en las siguientes tablas `data.sesgo_inequidad`, `test.pruebas_unitarias`, `metadata.metadata_sesgo_inequidad`

### Monitoreo entrenamiento
Una vez entrenado el modelo y haber seleccionado uno de ellos, estaríamos interesados en verificar que el último momento en que se entrenó el modelo corresponde en proporción a cómo está prediciendo el mismo, para esto generamos una tabla en el esquema _monitoreo_ que se llama _restaurante_scores_ que eventualmente también servirá para desplegar nuestro dashboard. La forma de correr esta tarea es la siguiente:
```
PYTHONPATH="." luigi --module src.pipeline.monitoreo_entrenamiento monitoreo_entrena --tipo-ingesta consecutiva --fecha 2021-04-23T00:00:00.00 --bucket data-product-architecture-equipo8 --tamanio 100 --proceso entrenamiento
```

## Rama 2. Predicción

### Predicción
Esta parte se refiere a la salida del algoritmo elegido (en la parte de selección) después de haber sido entrenado en el conjunto de datos históricos y aplicado a nuevos datos al pronosticar la probabilidad de un resultado en particular, en este caso, si el restaurante pasará o no la inspección.

Para ejecutar la tarea de predicción, corremos lo siguiente:
```
PYTHONPATH="." luigi --module src.pipeline.metadata_predecir metadata_predice --tipo-ingesta consecutiva --fecha 2021-04-30T00:00:00.00 --bucket data-product-architecture-equipo8 --tamanio 100 --tipo-prueba infinito --proceso prediccion
```
Esta tarea creará registros en las siguientes tablas `data.prediccion`, `metadata.metadata_prediccion`.

Para ejemplificar la prueba unitaria de este proceso, podemos correr el siguiente código, el cual fallará debido a la forma de la tabla porque espera un resultado con una forma de 1x1.
```
PYTHONPATH="." luigi --module src.pipeline.test_predecir test_prediccion --tipo-ingesta consecutiva --fecha 2021-04-30T00:00:00.00 --bucket data-product-architecture-equipo8 --tamanio 100 --tipo-prueba shape --proceso prediccion
```

### Almacenamiento API

Para poder exponer nuestro producto de datos creamos una API en **Flask** y adicionalmente la expondremos de una forma didáctica con _flask-restplus_, para esto creamos un nuevo esquema en nuestra base de datos llamado _api_ con la tabla _api_prediccion_ y se guardan los datos de este proceso de predicción.

Guardamos esa información corriendo lo siguiente:
```
PYTHONPATH="." luigi --module src.pipeline.almacena_api api --tipo-ingesta consecutiva --fecha 2021-04-30T00:00:00.00 --bucket data-product-architecture-equipo8 --tamanio 100 --tipo-prueba infinito --proceso prediccion
```
Más adelante explicaremos cómo interactuar con **Flask**.

### Monitoreo predicción

En esta tarea insertamos nuevos datos a la tabla de _restaurante_scores_ que se encuentra en el esquema _monitoreo_ para poder validar que efectivamente la predicción se está comportando de una manera similar al entrenamiento, esta tabla será usada por **Dash**, para tener nuestro monitoreo de una forma más visual, esto se logra corriendo la siguiente sentencia:
```
PYTHONPATH="." luigi --module src.pipeline.monitoreo_prediccion monitoreo_predice --tipo-ingesta consecutiva --fecha 2021-04-30T00:00:00.00 --bucket data-product-architecture-equipo8 --tamanio 100 --tipo-prueba infinito --proceso prediccion
```

## DAG en Luigi
Si las sentencias anteriores se corren en el orden indicado, podremos ver el _DAG_ de Luigi de la rama de entrenamiento similar a este:

<img width="1020" alt="imagen" src="https://github.com/sancas96/DPA-Chicago-VLIN/blob/main/images/Checkpoint6.png">

Y el _DAG_ de la rama de prediccion, similar a este otro:

# Flask

Se cuentan con 2 endpoints de API:
+ Endpoint 1:
  + Input: id establecimiento y probabilidad.
  + Output: JSON con score de predicción, etiqueta predicha
  Como ejemplo se puede poner el id_establecimiento 33 o 55
+ Endpoint 2:
  + Input: fecha prediccion
  + Output: JSON con una lista que contienen para cada establecimiento que tiene una predicción para ese día: id establecimiento, score de predicción, etiqueta predicha.
  Como ejemplo se puede poner la fecha_prediccion `2021-04-30T00:00:00.00`

Dentro de la ruta del repo se corren las siguientes sentencias para lanzar **Flask**
```
export FLASK_APP=flask_app.py
flask run --host=0.0.0.0 --port=1234
```

## Dashboard

Dado que nuestro modelo ya se encuentra en producción, necesitamos monitorearlo porque es parte de un sistema dinámico y queremos estar al pendiente de cómo va el desempeño de nuestro modelo ante nuevos datos.

Corremos lo siguiente desde la EC2 y dentro de este repositorio:
```
python src/utils/dash_app.py
```
Esto ejecutará nuestra aplicación **Dash** en donde podremos ver una gráfica de comparación entre las predicciones que hizo nuestro modelo y lo que salió en el entrenamiento. Lo que esperamos es que no haya sobreajuste o subajuste, es decir, que ambos resultados sean similares para las categorías que se presenten, en este caso, para tipo de establecimiento.

---

**Figura 1**. Estructura básica del proyecto.

```  
├── README.md          <- Aquí se encuentra la explicación de este producto de datos.
├── conf
│   ├── base           <- Configuración de parámetros.
│   └── local          <- Se almacenan las llaves para interactuar con este producto de datos.
├── data               <- Guarda de manera local algunos archivos para la ejecución de las tareas.
│   └── luigi          <- Guarda archivos de ingesta de manera local.
├── images             <- Imágenes utilizadas en este repositorio.
├── notebooks          <- Notebook de análisis exploratorio.
├── requirements.txt   <- Archivo que indica todas las librerías usadas por python y  para actival el pyenv.
├── .gitignore         <- Indica qué archivos evitar subir cuando se hace push al repositorio.
├── infrastructure     <- Se encuentra la api de flask y dash.
├── sql                <- Características de cómo crear la base de datos.
└── src                <- Códigos fuentes usados en este proyecto.
    ├── etl            <- Transformación de datos.
    ├── pipeline       <- Scripts donde vienen todas la tareas de Luigi.
    └── utils          <- Scripts de funciones que ayudan al pipeline.
```
