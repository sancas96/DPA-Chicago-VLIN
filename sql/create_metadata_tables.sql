--Este script sirve para generar la base de datos , usuario, esquemas para el producto de datos.
--Estos son los esquemas.
create schema metadata authorization chicago_user;
create schema data authorization chicago_user;

--Estas son las tablas del esquema data.
create table data.limpieza
(
	"inspection_id" NUMERIC,
	"dba_name" VARCHAR,
	"aka_name" VARCHAR,
	"license_" NUMERIC,
	"facility_type" VARCHAR,
	"risk" VARCHAR,
	"address" VARCHAR,
	"city" VARCHAR,
	"state" VARCHAR,
	"zip" VARCHAR,
	"inspection_date" VARCHAR,
	"inspection_type" VARCHAR,
	"results" VARCHAR,
	"violations" VARCHAR,
	"latitude" NUMERIC,
	"longitude" NUMERIC,
	"location_latitude" NUMERIC,
	"location_longitude" NUMERIC
);

create table data.ingenieria 
(
	"dba_name" NUMERIC,
	"license_" NUMERIC,
	"facility_type" NUMERIC,
	"risk" NUMERIC,
	"address" NUMERIC,
	"zip" NUMERIC,
	"results" NUMERIC,
	"latitude" NUMERIC,
	"longitude" NUMERIC,
	"Approved_food_sources_1" NUMERIC,
	"Hot_cold_storage_facilities_2" NUMERIC,
	"Hot_cold_storage_temp_3" NUMERIC,
	"Contaminant_protection_4" NUMERIC,
	"No_sick_handlers_5" NUMERIC,
	"Proper_hand_washing_6" NUMERIC,
	"Proper_utensil_washing_7" NUMERIC,
	"Proper_sanitizing_solution_8" NUMERIC,
	"Hot_cold_water_supply_9" NUMERIC,
	"Waste_water_disposal_10" NUMERIC,
	"Adequate_toilet_facilities_11" NUMERIC,
	"Adequate_hand_washing_facilities_12" NUMERIC,
	"Control_of_rodents_other_pests_13" NUMERIC,
	"Correct_serious_violations_14" NUMERIC,
	"No_reserved_food_15" NUMERIC,
	"Protection_from_contamination_16" NUMERIC,
	"Proper_thawing_17" NUMERIC,
	"Pest_control_associated_areas_18" NUMERIC,
	"Proper_garbage_area_19" NUMERIC,
	"Proper_garbage_storage_20" NUMERIC,
	"Oversight_of_hazardous_food_21" NUMERIC,
	"Dishwasher_maintenance_22" NUMERIC,
	"Scrape_before_washing_23" NUMERIC,
	"Proper_dishwashers_24" NUMERIC,
	"Minimize_toxic_materials_25" NUMERIC,
	"Adequate_customer_toilets_26" NUMERIC,
	"Supplied_toilet_facilities_27" NUMERIC,
	"Visible_inspection_report_28" NUMERIC,
	"Correct_minor_violations_29" NUMERIC,
	"Labelled_containers_30" NUMERIC,
	"Sterile_utensils_31" NUMERIC,
	"Clean_maintain_equipment_32" NUMERIC,
	"Clean_sanitize_utensils_33" NUMERIC,
	"Clean_maintain_floor_34" NUMERIC,
	"Maintain_walls_ceiling_35" NUMERIC,
	"Proper_lighting_36" NUMERIC,
	"Toilet_rooms_vented_37" NUMERIC,
	"Proper_venting_plumbing_38" NUMERIC,
	"Linen_clothing_storage_39" NUMERIC,
	"Proper_thermometers_40" NUMERIC,
	"Clean_facilities_store_supplies_41" NUMERIC,
	"Ice_handling_hairnets_clothes_42" NUMERIC,
	"Ice_equipment_storage_43" NUMERIC,
	"Restrict_prep_area_traffic_44" NUMERIC,
	"Restrict_smoking_70" NUMERIC,
	"critical_count" NUMERIC,
	"serious_count" NUMERIC,
	"minor_count" NUMERIC
 );
 
--Estas son las tablas del esquema metadata.
create table metadata.metadata_ingesta
(
	"fecha_insercion" VARCHAR,
	"nombre" VARCHAR,
	"size" INTEGER,
	"filetype" VARCHAR
);

create table metadata.metadata_almacenamiento
(
	"fecha_insercion" VARCHAR,
	"size" INTEGER,
	"nombre" VARCHAR
);

create table metadata.metadata_limpieza
 (
	"fecha_insercion" VARCHAR,
	"num_registros" INTEGER,
	"fecha_max" VARCHAR
);

create table metadata.metadata_ingenieria
 (
	"fecha_insercion" VARCHAR,
	"num_registros" INTEGER,
	"critical_null" VARCHAR,
	"serious_null" VARCHAR,
	"minor_null" VARCHAR,
);