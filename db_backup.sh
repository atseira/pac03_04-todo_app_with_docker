#!/bin/bash

# Define the backup directory
BACKUP_DIR="./backups"

# Define the database connection details
DB_HOST="localhost"
DB_PORT="5433"
DB_NAME="test"
DB_USER="postgres"
DB_PASSWORD="password"

# Generate a timestamp for the backup file
TIMESTAMP=$(date +"%Y%m%d%H%M%S")

# Define the backup filename with timestamp
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.sql"

# Perform the backup using pg_dump
pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -F p > "$BACKUP_FILE"

# Check if the backup was successful
if [ $? -eq 0 ]; then
    echo "Database backup created successfully: $BACKUP_FILE"
else
    echo "Error creating database backup!"
fi
