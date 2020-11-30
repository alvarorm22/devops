#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
   CREATE TABLE measureslog(timestamp TIMESTAMP,id_entity TEXT NOT NULL,so2 DOUBLE PRECISION,no2 DOUBLE PRECISION,co DOUBLE PRECISION,o3 DOUBLE PRECISION,pm10 DOUBLE PRECISION,pm2_5 DOUBLE PRECISION);
   COPY measureslog(timestamp,id_entity,so2,no2,co,o3,pm10,pm2_5) FROM '/environment_airq_measurand.csv' DELIMITER ',' CSV HEADER;
EOSQL
