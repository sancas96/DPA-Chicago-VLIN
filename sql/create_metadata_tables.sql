
drop schema if exists raw cascade;
create schema raw;

drop schema if exists cleaned cascade;
create schema cleaned;

drop schema if exists semantic cascade;
create schema semantic;


create schema if not exists raw;
drop table if exists raw.Chicago_food;
create table raw.Chicago_food (
  "col_1" VARCHAR,
  "col_2" VARCHAR);
