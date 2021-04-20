
drop schema if exists raw cascade;
create schema raw;


drop schema if exists cleaned cascade;
create schema cleaned;


drop schema if exists semantic cascade;
create schema semantic;


create schema if not exists raw;


drop table if exists raw.Ingesta;
create table raw.Ingesta (
  "fecha_insercion" VARCHAR,
  "nombre" VARCHAR,
  "size" INTEGER,
  "filetype" VARCHAR);
  
comment on table raw.Ingesta is 'describe las caracteristicas de la Ingesta';  
 
 
drop table if exists raw.Almacenamiento;
create table raw.Almacenamiento(
  "fecha_insercion" VARCHAR,
  "size" INTEGER,
  "nombre" VARCHAR);
 
 comment on table raw.Almacenamiento is 'describe las caracteristicas del Almacenamiento';


drop table if exists raw.Limpieza;
create table raw.Limpieza (
  "fecha_insercion" VARCHAR,
  "num_registros" INTEGER,
  "fecha_max" VARCHAR); 
  
 comment on table raw.Limpieza is 'describe las caracteristicas de la Limpieza';
 

drop table if exists raw.Ingenieria;
create table raw.Ingenieria (
  "fecha_insercion" VARCHAR,
  "num_registros" INTEGER,
  "critical_null" VARCHAR,
  "serious_null" VARCHAR,
  "minor_null" VARCHAR); 
  
 comment on table raw.Limpieza is 'describe las caracteristicas de la Ingeniaria';

