#!/bin/bash

NAMESPACE="default"
LOG_FILE="/opt/scripts/pod_health_check.log"
DATE=$(date "+%Y-%m-%d %H:%M:%S")

echo "[$DATE] Starting Kubernetes health check..." >> $LOG_FILE

# List pods that are not Running or Completed
for pod in $(kubectl get pods -n $NAMESPACE --no-headers | awk '$3!="Running" && $3!="Completed"{print $1}'); do
    STATUS=$(kubectl get pod $pod -n $NAMESPACE -o jsonpath='{.status.phase}')
    echo "[$DATE] Pod: $pod | Status: $STATUS" >> $LOG_FILE

    # Restart the unhealthy pod
    kubectl delete pod $pod -n $NAMESPACE --grace-period=0 --force
    echo "[$DATE] Restarted pod: $pod" >> $LOG_FILE
done

echo "[$DATE] Health check completed." >> $LOG_FILE

# End of script