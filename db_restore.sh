#!/bin/bash

# Define the backup directory
BACKUP_DIR="./backups"

# Define the database connection details
DB_HOST="localhost"
DB_PORT="5433"
DB_NAME="test"
DB_USER="postgres"
DB_PASSWORD="password"

# Prompt the user to enter the backup file path
read -p "Enter the path to the backup file: " BACKUP_FILE

# Check if the backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo "Backup file not found: $BACKUP_FILE"
fi

# Perform the database restore using psql
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f "$BACKUP_FILE"

# Check if the restore was successful
if [ $? -eq 0 ]; then
    echo "Database restored successfully."
else
    echo "Error restoring database!"
fi
