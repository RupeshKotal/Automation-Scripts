#!/bin/bash

# Directories
LOG_DIR="/opt/utxapp/logs"
BACKUP_DIR="/opt/utxapp/backup"
RETENTION_DAYS=7
DATE=$(date +%F)

# Create backup dir if not exists
mkdir -p $BACKUP_DIR

# Compress old logs
find $LOG_DIR -type f -name "*.log" -mtime +0 -exec gzip {} \;

# Move compressed logs to backup folder
find $LOG_DIR -type f -name "*.gz" -exec mv {} $BACKUP_DIR/ \;

# Delete backups older than 7 days
find $BACKUP_DIR -type f -mtime +$RETENTION_DAYS -delete

# Log action
echo "[$(date)] Log rotation completed. Old logs moved to $BACKUP_DIR" >> $BACKUP_DIR/backup.log
