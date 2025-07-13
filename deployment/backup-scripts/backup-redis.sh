#!/bin/bash

# Hawaiian LeniLani Redis Backup Script
# Runs in Hawaii Standard Time (HST)

set -e

# Configuration
REDIS_HOST="${REDIS_HOST:-redis}"
REDIS_PORT="${REDIS_PORT:-6379}"
REDIS_PASSWORD="${REDIS_PASSWORD}"

BACKUP_DIR="/backup/redis"
LOG_DIR="/backup/logs"
S3_BUCKET="${S3_BACKUP_BUCKET}"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-7}"

# Create directories if they don't exist
mkdir -p "$BACKUP_DIR" "$LOG_DIR"

# Get current timestamp in HST
TIMESTAMP=$(TZ='Pacific/Honolulu' date +%Y%m%d_%H%M%S)
BACKUP_FILE="hawaiian_lenilani_redis_${TIMESTAMP}.rdb.gz"
LOG_FILE="$LOG_DIR/redis_backup_${TIMESTAMP}.log"

# Function to log messages
log() {
    echo "[$(TZ='Pacific/Honolulu' date '+%Y-%m-%d %H:%M:%S HST')] $1" | tee -a "$LOG_FILE"
}

# Start backup
log "Starting Redis backup for Hawaiian LeniLani cache"
log "Aloha! Backing up Redis instance at $REDIS_HOST:$REDIS_PORT"

# Build Redis CLI command
REDIS_CLI_CMD="redis-cli -h $REDIS_HOST -p $REDIS_PORT"
if [ -n "$REDIS_PASSWORD" ]; then
    REDIS_CLI_CMD="$REDIS_CLI_CMD -a $REDIS_PASSWORD"
fi

# Trigger Redis background save
log "Triggering Redis background save (BGSAVE)..."
if $REDIS_CLI_CMD BGSAVE 2>/dev/null; then
    log "Background save initiated"
else
    log "ERROR: Failed to initiate Redis background save!"
    exit 1
fi

# Wait for background save to complete
log "Waiting for background save to complete..."
while [ "$($REDIS_CLI_CMD LASTSAVE 2>/dev/null)" = "$LAST_SAVE_TIME" ]; do
    sleep 1
done

# Get Redis data directory
REDIS_DIR=$($REDIS_CLI_CMD CONFIG GET dir 2>/dev/null | tail -1)
REDIS_DBFILE=$($REDIS_CLI_CMD CONFIG GET dbfilename 2>/dev/null | tail -1)

log "Redis data located at: $REDIS_DIR/$REDIS_DBFILE"

# Create temporary copy and compress
TEMP_FILE="/tmp/redis_backup_${TIMESTAMP}.rdb"
if $REDIS_CLI_CMD --rdb "$TEMP_FILE" 2>/dev/null; then
    log "Redis dump created successfully"
    
    # Compress the backup
    if gzip -9 < "$TEMP_FILE" > "$BACKUP_DIR/$BACKUP_FILE"; then
        log "Backup compressed successfully: $BACKUP_FILE"
        log "Backup size: $(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)"
        rm -f "$TEMP_FILE"
    else
        log "ERROR: Failed to compress backup!"
        rm -f "$TEMP_FILE"
        exit 1
    fi
else
    log "ERROR: Failed to create Redis dump!"
    exit 1
fi

# Get Redis statistics
REDIS_INFO=$($REDIS_CLI_CMD INFO 2>/dev/null)
USED_MEMORY=$(echo "$REDIS_INFO" | grep "used_memory_human:" | cut -d: -f2 | tr -d '\r')
TOTAL_KEYS=$($REDIS_CLI_CMD DBSIZE 2>/dev/null | cut -d' ' -f1)

log "Redis statistics:"
log "  - Used memory: $USED_MEMORY"
log "  - Total keys: $TOTAL_KEYS"

# Upload to S3 if configured
if [ -n "$S3_BUCKET" ]; then
    log "Uploading backup to S3 bucket: $S3_BUCKET"
    if aws s3 cp "$BACKUP_DIR/$BACKUP_FILE" "s3://$S3_BUCKET/redis/$BACKUP_FILE" \
        --storage-class STANDARD_IA \
        --metadata "timestamp=$TIMESTAMP,used_memory=$USED_MEMORY,total_keys=$TOTAL_KEYS"; then
        log "Backup uploaded to S3 successfully"
    else
        log "WARNING: S3 upload failed, keeping local backup"
    fi
fi

# Clean up old local backups
log "Cleaning up backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -name "hawaiian_lenilani_redis_*.rdb.gz" -mtime +$RETENTION_DAYS -delete

# Update last backup timestamp
echo "$TIMESTAMP" > "$LOG_DIR/last-redis-backup.log"

# Log backup statistics
BACKUP_COUNT=$(find "$BACKUP_DIR" -name "hawaiian_lenilani_redis_*.rdb.gz" | wc -l)
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)

log "Redis backup completed successfully!"
log "Total backups: $BACKUP_COUNT"
log "Total backup size: $TOTAL_SIZE"
log "Mahalo! Hawaiian LeniLani Redis backup pau (finished)"

# Send notification if webhook configured
if [ -n "$BACKUP_WEBHOOK_URL" ]; then
    curl -s -X POST "$BACKUP_WEBHOOK_URL" \
        -H "Content-Type: application/json" \
        -d "{
            \"text\": \"Hawaiian LeniLani Redis Backup Completed\",
            \"timestamp\": \"$TIMESTAMP\",
            \"file\": \"$BACKUP_FILE\",
            \"size\": \"$(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)\",
            \"used_memory\": \"$USED_MEMORY\",
            \"total_keys\": \"$TOTAL_KEYS\",
            \"status\": \"success\"
        }" > /dev/null 2>&1 || true
fi

exit 0