#!/bin/bash

# Hawaiian LeniLani PostgreSQL Restore Script
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

# Function to log messages
log() {
    echo "[$(TZ='Pacific/Honolulu' date '+%Y-%m-%d %H:%M:%S HST')] $1"
}

# Check if backup file is provided
if [ -z "$1" ]; then
    log "ERROR: No backup file specified!"
    log "Usage: $0 <backup_file> [from_s3]"
    log ""
    log "Available local backups:"
    ls -la "$BACKUP_DIR"/hawaiian_lenilani_backup_*.sql.gz 2>/dev/null || echo "No local backups found"
    exit 1
fi

BACKUP_FILE="$1"
FROM_S3="${2:-false}"

# Start restore
log "Starting PostgreSQL restore for Hawaiian LeniLani database"
log "E komo mai! Restoring database: $DB_NAME"

# Set PostgreSQL password
export PGPASSWORD="$DB_PASSWORD"

# Download from S3 if specified
if [ "$FROM_S3" = "from_s3" ] || [ "$FROM_S3" = "true" ]; then
    if [ -z "$S3_BUCKET" ]; then
        log "ERROR: S3_BUCKET not configured!"
        exit 1
    fi
    
    log "Downloading backup from S3..."
    TEMP_FILE="/tmp/$BACKUP_FILE"
    if aws s3 cp "s3://$S3_BUCKET/postgres/$BACKUP_FILE" "$TEMP_FILE"; then
        log "Backup downloaded successfully from S3"
        RESTORE_FILE="$TEMP_FILE"
    else
        log "ERROR: Failed to download backup from S3!"
        exit 1
    fi
else
    # Use local file
    RESTORE_FILE="$BACKUP_DIR/$BACKUP_FILE"
    if [ ! -f "$RESTORE_FILE" ]; then
        log "ERROR: Backup file not found: $RESTORE_FILE"
        exit 1
    fi
fi

log "Restore file: $RESTORE_FILE"
log "File size: $(du -h "$RESTORE_FILE" | cut -f1)"

# Create restore log
TIMESTAMP=$(TZ='Pacific/Honolulu' date +%Y%m%d_%H%M%S)
RESTORE_LOG="$LOG_DIR/restore_${TIMESTAMP}.log"

# Confirm restore
log "WARNING: This will restore the database from backup!"
log "Current database '$DB_NAME' will be overwritten."
log "Press Ctrl+C to cancel, or wait 10 seconds to continue..."
sleep 10

# Check database connection
log "Checking database connection..."
if psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres -c "SELECT 1" > /dev/null 2>&1; then
    log "Database connection successful"
else
    log "ERROR: Cannot connect to database!"
    exit 1
fi

# Drop existing connections to the database
log "Dropping existing connections to database..."
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres <<EOF
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = '$DB_NAME' AND pid <> pg_backend_pid();
EOF

# Restore database
log "Starting database restore..."
if gunzip -c "$RESTORE_FILE" | psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
    --single-transaction --quiet > "$RESTORE_LOG" 2>&1; then
    
    log "Database restored successfully!"
    
    # Run post-restore checks
    log "Running post-restore checks..."
    
    # Check table counts
    TABLE_COUNT=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c \
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema IN ('chatbot', 'analytics')")
    log "Tables restored: $TABLE_COUNT"
    
    # Check conversation count
    CONV_COUNT=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c \
        "SELECT COUNT(*) FROM chatbot.conversations" 2>/dev/null || echo "0")
    log "Conversations restored: $CONV_COUNT"
    
    # Check lead count
    LEAD_COUNT=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c \
        "SELECT COUNT(*) FROM chatbot.leads" 2>/dev/null || echo "0")
    log "Leads restored: $LEAD_COUNT"
    
else
    log "ERROR: Database restore failed!"
    log "Check restore log: $RESTORE_LOG"
    tail -20 "$RESTORE_LOG"
    exit 1
fi

# Clean up temporary file
if [ -n "$TEMP_FILE" ] && [ -f "$TEMP_FILE" ]; then
    rm -f "$TEMP_FILE"
fi

# Update analytics
log "Updating analytics views..."
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" <<EOF
REFRESH MATERIALIZED VIEW CONCURRENTLY analytics.daily_conversations;
REFRESH MATERIALIZED VIEW CONCURRENTLY analytics.island_metrics;
REFRESH MATERIALIZED VIEW CONCURRENTLY analytics.service_performance;
EOF

log "Restore completed successfully!"
log "Mahalo! Hawaiian LeniLani database restore pau (finished)"

# Log restore event
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" <<EOF
INSERT INTO analytics.events (event_type, event_data) 
VALUES ('database_restored', 
    '{"backup_file": "$BACKUP_FILE", "restore_timestamp": "$TIMESTAMP", "conversation_count": $CONV_COUNT, "lead_count": $LEAD_COUNT}'::jsonb);
EOF

# Send notification if webhook configured
if [ -n "$BACKUP_WEBHOOK_URL" ]; then
    curl -s -X POST "$BACKUP_WEBHOOK_URL" \
        -H "Content-Type: application/json" \
        -d "{
            \"text\": \"Hawaiian LeniLani Database Restore Completed\",
            \"timestamp\": \"$TIMESTAMP\",
            \"backup_file\": \"$BACKUP_FILE\",
            \"conversation_count\": $CONV_COUNT,
            \"lead_count\": $LEAD_COUNT,
            \"status\": \"success\"
        }" > /dev/null 2>&1 || true
fi

exit 0