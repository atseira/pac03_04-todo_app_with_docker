#!/bin/bash

# Define the database connection details
DB_HOST="localhost"
DB_PORT="5433"
DB_NAME="test"
DB_USER="postgres"
DB_PASSWORD="password"

export PGPASSWORD="${DB_PASSWORD}"

psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" -c "
DO \$\$ DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END \$\$;"
