#!/bin/bash

# Hawaiian LeniLani PostgreSQL Backup Script
# Runs in Hawaii Standard Time (HST)

set -e

# Configuration
DB_HOST="${POSTGRES_HOST:-postgres}"
DB_PORT="${POSTGRES_PORT:-5432}"
DB_NAME="${POSTGRES_DB:-hawaiian_lenilani}"
DB_USER="${POSTGRES_USER:-lenilani}"
DB_PASSWORD="${POSTGRES_PASSWORD}"

BACKUP_DIR="/backup/postgres"
LOG_DIR="/backup/logs"
S3_BUCKET="${S3_BACKUP_BUCKET}"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-7}"

# Create directories if they don't exist
mkdir -p "$BACKUP_DIR" "$LOG_DIR"

# Get current timestamp in HST
TIMESTAMP=$(TZ='Pacific/Honolulu' date +%Y%m%d_%H%M%S)
BACKUP_FILE="hawaiian_lenilani_backup_${TIMESTAMP}.sql.gz"
LOG_FILE="$LOG_DIR/backup_${TIMESTAMP}.log"

# Function to log messages
log() {
    echo "[$(TZ='Pacific/Honolulu' date '+%Y-%m-%d %H:%M:%S HST')] $1" | tee -a "$LOG_FILE"
}

# Start backup
log "Starting PostgreSQL backup for Hawaiian LeniLani database"
log "Aloha! Backing up database: $DB_NAME"

# Set PostgreSQL password
export PGPASSWORD="$DB_PASSWORD"

# Perform backup
log "Creating database dump..."
if pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
    --no-owner --no-privileges --clean --if-exists \
    --exclude-schema=pg_catalog --exclude-schema=information_schema \
    | gzip -9 > "$BACKUP_DIR/$BACKUP_FILE"; then
    
    log "Database backup created successfully: $BACKUP_FILE"
    log "Backup size: $(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)"
else
    log "ERROR: Database backup failed!"
    exit 1
fi

# Upload to S3 if configured
if [ -n "$S3_BUCKET" ]; then
    log "Uploading backup to S3 bucket: $S3_BUCKET"
    if aws s3 cp "$BACKUP_DIR/$BACKUP_FILE" "s3://$S3_BUCKET/postgres/$BACKUP_FILE" \
        --storage-class STANDARD_IA \
        --metadata "timestamp=$TIMESTAMP,database=$DB_NAME"; then
        log "Backup uploaded to S3 successfully"
    else
        log "WARNING: S3 upload failed, keeping local backup"
    fi
fi

# Clean up old local backups
log "Cleaning up backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -name "hawaiian_lenilani_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete

# Clean up old logs
find "$LOG_DIR" -name "backup_*.log" -mtime +30 -delete

# Update last backup timestamp
echo "$TIMESTAMP" > "$LOG_DIR/last-backup.log"

# Log backup statistics
BACKUP_COUNT=$(find "$BACKUP_DIR" -name "hawaiian_lenilani_backup_*.sql.gz" | wc -l)
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)

log "Backup completed successfully!"
log "Total backups: $BACKUP_COUNT"
log "Total backup size: $TOTAL_SIZE"
log "Mahalo! Hawaiian LeniLani database backup pau (finished)"

# Send notification if webhook configured
if [ -n "$BACKUP_WEBHOOK_URL" ]; then
    curl -s -X POST "$BACKUP_WEBHOOK_URL" \
        -H "Content-Type: application/json" \
        -d "{
            \"text\": \"Hawaiian LeniLani Database Backup Completed\",
            \"timestamp\": \"$TIMESTAMP\",
            \"database\": \"$DB_NAME\",
            \"file\": \"$BACKUP_FILE\",
            \"size\": \"$(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)\",
            \"status\": \"success\"
        }" > /dev/null 2>&1 || true
fi

exit 0