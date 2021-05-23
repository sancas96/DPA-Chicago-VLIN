#Este task genera las predicciones del mejor modelo seleccionado, dado un data set nuevo que pasó por limpieza e ingeniería de características
import luigi
import pickle
import pandas as pd
import boto3
from luigi.contrib.postgres import CopyToTable
from src.utils.general import *
from src.pipeline.metadata_ingenieria_caract import metadata_ingenieria

class predice(CopyToTable):
    #Parámetros de las tareas anteriores
    tipo_ingesta = luigi.Parameter() #Puede ser "historica" o "consecutiva".
    fecha = luigi.Parameter() #Fecha en la que se está haciendo la ingesta con respecto a inspection date.
    bucket = luigi.Parameter()
    tamanio= luigi.IntParameter()
    proceso= luigi.Parameter() #Puede ser "entrenamiento" o "prediccion"
    
    #Obteniendo las credenciales para conectarse a la base de datos de chicago
    db_creds = get_database_connection('conf/local/credentials.yaml')
    user = db_creds['user']
    password = db_creds['password']
    database = db_creds['database']
    host = db_creds['host']
    port = db_creds['port']

    #Tabla y columnas donde se creará la tabla predicción
    table = 'data.prediccion'
    columns = [
                ('fecha_parametro','VARCHAR'),
                ('inspection_id', 'NUMERIC'),
                ('dba_name', 'NUMERIC'),
                ('license_', 'NUMERIC'),
                ('facility_type', 'VARCHAR'),
                ('risk', 'NUMERIC'),
                ('address', 'NUMERIC'),
                ('zip', 'NUMERIC'),
                ('results', 'NUMERIC'),
                ('latitude', 'NUMERIC'),
                ('longitude', 'NUMERIC'),
                ('Approved_food_sources_1', 'NUMERIC'),
                ('Hot_cold_storage_facilities_2', 'NUMERIC'),
                ('Hot_cold_storage_temp_3', 'NUMERIC'),
                ('Contaminant_protection_4', 'NUMERIC'),
                ('No_sick_handlers_5', 'NUMERIC'),
                ('Proper_hand_washing_6', 'NUMERIC'),
                ('Proper_utensil_washing_7', 'NUMERIC'),
                ('Proper_sanitizing_solution_8', 'NUMERIC'),
                ('Hot_cold_water_supply_9', 'NUMERIC'),
                ('Waste_water_disposal_10', 'NUMERIC'),
                ('Adequate_toilet_facilities_11', 'NUMERIC'),
                ('Adequate_hand_washing_facilities_12', 'NUMERIC'),
                ('Control_of_rodents_other_pests_13', 'NUMERIC'),
                ('Correct_serious_violations_14', 'NUMERIC'),
                ('No_reserved_food_15', 'NUMERIC'),
                ('Protection_from_contamination_16', 'NUMERIC'),
                ('Proper_thawing_17', 'NUMERIC'),
                ('Pest_control_associated_areas_18', 'NUMERIC'),
                ('Proper_garbage_area_19', 'NUMERIC'),
                ('Proper_garbage_storage_20', 'NUMERIC'),
                ('Oversight_of_hazardous_food_21', 'NUMERIC'),
                ('Dishwasher_maintenance_22', 'NUMERIC'),
                ('Scrape_before_washing_23', 'NUMERIC'),
                ('Proper_dishwashers_24', 'NUMERIC'),
                ('Minimize_toxic_materials_25', 'NUMERIC'),
                ('Adequate_customer_toilets_26', 'NUMERIC'),
                ('Supplied_toilet_facilities_27', 'NUMERIC'),
                ('Visible_inspection_report_28', 'NUMERIC'),
                ('Correct_minor_violations_29', 'NUMERIC'),
                ('Labelled_containers_30', 'NUMERIC'),
                ('Sterile_utensils_31', 'NUMERIC'),
                ('Clean_maintain_equipment_32', 'NUMERIC'),
                ('Clean_sanitize_utensils_33', 'NUMERIC'),
                ('Clean_maintain_floor_34', 'NUMERIC'),
                ('Maintain_walls_ceiling_35', 'NUMERIC'),
                ('Proper_lighting_36', 'NUMERIC'),
                ('Toilet_rooms_vented_37', 'NUMERIC'),
                ('Proper_venting_plumbing_38', 'NUMERIC'),
                ('Linen_clothing_storage_39', 'NUMERIC'),
                ('Proper_thermometers_40', 'NUMERIC'),
                ('Clean_facilities_store_supplies_41', 'NUMERIC'),
                ('Ice_handling_hairnets_clothes_42', 'NUMERIC'),
                ('Ice_equipment_storage_43', 'NUMERIC'),
                ('Restrict_prep_area_traffic_44', 'NUMERIC'),
                ('Restrict_smoking_70', 'NUMERIC'),
                ('critical_count', 'NUMERIC'),
                ('serious_count', 'NUMERIC'),
                ('minor_count', 'NUMERIC'),
                ('prediccion', 'NUMERIC'),
                ('prediccion_proba', 'NUMERIC')
              ]

    def requires(self):
        return metadata_ingenieria(self.tipo_ingesta, self.fecha, self.bucket, self.tamanio)


    def rows(self):
        if self.proceso=='prediccion':
            #Obtenemos la predicción del último mejor modelo.
            s3_creds = get_s3_credentials('conf/local/credentials.yaml')
            session = boto3.Session(aws_access_key_id=s3_creds['aws_access_key_id'],
                                        aws_secret_access_key=s3_creds['aws_secret_access_key'])
            cliente_s3 = session.client('s3')
            lista_archivos = cliente_s3.list_objects_v2(Bucket = f"{self.bucket}", Prefix = 'seleccion')['Contents']
            fecha_ultimo = max(lista_archivos, key=lambda x: x['LastModified'])['Key'][-38:-16]
            objeto_s3 = cliente_s3.get_object(
                                                Bucket=f"{self.bucket}",
                                                Key=f"seleccion/{fecha_ultimo}-MejorModelo.pkl"
                                             )
            contenido_objeto=objeto_s3['Body'].read()
            datos_predic= pd.DataFrame(query_database(f"SELECT * from data.ingenieria where fecha_parametro='{self.fecha}';"))
            datos_predic.columns=[i[0] for i in query_database("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS where table_name='ingenieria';")]
            datos_predic[datos_predic.columns]=datos_predic[datos_predic.columns].apply(pd.to_numeric, errors='coerce')
            datos_predic=datos_predic.fillna(0)
            prediccion=pickle.loads(contenido_objeto).predict(datos_predic.drop(['results'], axis=1))
            prob_prediccion=[r[1] for r in pickle.loads(contenido_objeto).predict_proba(datos_predic.drop(['results'], axis=1))]
            

            lista_ingenieria=datos_predic.values.tolist()
            lista_prediccion=prediccion.tolist()
            
            for i in range(len(lista_ingenieria)):
                lista_ingenieria[i][0]=self.fecha
                lista_ingenieria[i].append(lista_prediccion[i])
                lista_ingenieria[i].append(prob_prediccion[i])

            print('#######lista_ingenieria',lista_ingenieria[1])                                

            for element in lista_ingenieria:
                yield element
        else:
            exit()
