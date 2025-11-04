#!/bin/bash

# Variables
SERVICE_NAME="utxapp"
APP_URL="http://localhost:8080/health"
PORT=8080
LOG_FILE="/opt/scripts/deploy_verify.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$DATE] Starting deployment verification for $SERVICE_NAME..." >> $LOG_FILE

# Check if process is running
if pgrep -f "$SERVICE_NAME" > /dev/null; then
    echo "[$DATE] ✅ Process for $SERVICE_NAME is running." >> $LOG_FILE
else
    echo "[$DATE] ❌ Process for $SERVICE_NAME not found!" >> $LOG_FILE
    echo "[$DATE] ALERT: Process missing!" | mail -s "ALERT: $SERVICE_NAME process down" admin@company.com
fi

# Check if port is listening
if netstat -tuln | grep -q ":$PORT"; then
    echo "[$DATE] ✅ Port $PORT is listening." >> $LOG_FILE
else
    echo "[$DATE] ❌ Port $PORT not listening!" >> $LOG_FILE
    echo "[$DATE] ALERT: Port $PORT not listening!" | mail -s "ALERT: $SERVICE_NAME port issue" admin@company.com
fi

# Check health endpoint
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$APP_URL")
if [ "$HTTP_STATUS" -eq 200 ]; then
    echo "[$DATE] ✅ Health check passed (HTTP 200)." >> $LOG_FILE
else
    echo "[$DATE] ❌ Health check failed (HTTP $HTTP_STATUS)." >> $LOG_FILE
    echo "[$DATE] ALERT: Health check failed!" | mail -s "ALERT: $SERVICE_NAME health check failed" admin@company.com
fi

echo "[$DATE] Verification complete for $SERVICE_NAME." >> $LOG_FILE
