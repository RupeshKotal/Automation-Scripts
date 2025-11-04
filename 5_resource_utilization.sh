#!/bin/bash

# Threshold values (percentages)
THRESHOLD_CPU=80
THRESHOLD_MEM=80
THRESHOLD_DISK=90

# Log file to store monitoring results
LOG_FILE="/opt/scripts/resource_monitor.log"

# Current date/time
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# --- Collect System Metrics ---

# CPU Usage
CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print 100 - $8"%"}' | cut -d'.' -f1)

# Memory Usage
MEM=$(free | awk '/Mem/{printf("%.0f"), $3/$2 * 100}')

# Disk Usage for root filesystem
DISK=$(df -h / | awk 'NR==2{print $5}' | sed 's/%//')

# --- Log current status ---
echo "[$DATE] CPU: $CPU%, MEM: $MEM%, DISK: $DISK%" >> $LOG_FILE

# --- Check Thresholds and Send Alerts ---
if [ "$CPU" -ge "$THRESHOLD_CPU" ]; then
  echo "High CPU usage detected: $CPU%" | mail -s "ALERT: CPU High on $(hostname)" admin@company.com
fi

if [ "$MEM" -ge "$THRESHOLD_MEM" ]; then
  echo "High Memory usage detected: $MEM%" | mail -s "ALERT: Memory High on $(hostname)" admin@company.com
fi

if [ "$DISK" -ge "$THRESHOLD_DISK" ]; then
  echo "High Disk usage detected: $DISK%" | mail -s "ALERT: Disk Space Low on $(hostname)" admin@company.com
fi
