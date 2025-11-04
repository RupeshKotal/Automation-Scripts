Perfect — here’s your **Server Resource Utilization Monitoring Script (Shell)** written in clean, GitHub-ready `README.md` format, consistent with your previous automations:

---

````markdown
# 🧩 Automation #5: Server Resource Utilization Monitoring Script (Shell)

## 🧾 Problem

Before full observability or monitoring tools like Prometheus or CloudWatch were in place,  
we needed a **lightweight solution** to monitor **CPU, Memory, and Disk utilization** directly on EC2 servers.  

So, I wrote a **Shell script** that runs every few minutes, logs system metrics, and sends alerts when thresholds are crossed.

---

## ⚙️ Shell Script: `resource_monitor.sh`

```bash
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
````

---

## 🕒 Cron Schedule

Run every 5 minutes to track live server metrics:

```bash
*/5 * * * * /opt/scripts/resource_monitor.sh
```

---

## 🧠 Detailed Explanation of Each Section

### 🔹 1. Thresholds

```bash
THRESHOLD_CPU=80
THRESHOLD_MEM=80
THRESHOLD_DISK=90
```

Set the limits for triggering alerts:

* If **CPU > 80%**, send an alert
* If **Memory > 80%**, send an alert
* If **Disk > 90%**, send an alert

These can be adjusted per environment (staging vs. production).

---

### 🔹 2. Logging Setup

```bash
LOG_FILE="/opt/scripts/resource_monitor.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')
```

Keeps a **timestamped record** of CPU, memory, and disk metrics for auditing and troubleshooting.
Useful for identifying historical spikes or trends.

---

### 🔹 3. CPU Usage Command

```bash
CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print 100 - $8"%"}' | cut -d'.' -f1)
```

**Breakdown:**

* `top -bn1` → Runs `top` in batch mode for one iteration
* `grep "Cpu(s)"` → Filters the CPU summary line
* `$8` → Represents *idle* CPU percentage
* `100 - $8` → Calculates *used* CPU percentage
* `cut -d'.' -f1` → Removes decimal part for easy comparison

✅ **Example:**
If idle = 87%, usage = 13%

---

### 🔹 4. Memory Usage Command

```bash
MEM=$(free | awk '/Mem/{printf("%.0f"), $3/$2 * 100}')
```

**Breakdown:**

* `free` → Displays memory usage
* `$2` → Total memory
* `$3` → Used memory
* `$3/$2 * 100` → Percentage of memory used

✅ **Example:**
If total = 1024 MB and used = 800 MB → 78%

---

### 🔹 5. Disk Usage Command

```bash
DISK=$(df -h / | awk 'NR==2{print $5}' | sed 's/%//')
```

**Breakdown:**

* `df -h /` → Checks disk usage for root `/`
* `awk 'NR==2{print $5}'` → Extracts the usage percentage
* `sed 's/%//'` → Removes the `%` sign for numeric comparison

✅ **Example:**
Output = `85` → means **85% disk used**

---

### 🔹 6. Logging Output

```bash
echo "[$DATE] CPU: $CPU%, MEM: $MEM%, DISK: $DISK%" >> $LOG_FILE
```

Appends system status with timestamp to the log file.
Example log entry:

```
[2025-11-04 11:30:00] CPU: 23%, MEM: 72%, DISK: 81%
```

---

### 🔹 7. Alerting

```bash
if [ "$CPU" -ge "$THRESHOLD_CPU" ]; then
  echo "High CPU usage detected: $CPU%" | mail -s "ALERT: CPU High on $(hostname)" admin@company.com
fi
```

Uses the Linux `mail` command to notify admins when resource usage exceeds thresholds.
You can replace this with **Slack webhook**, **AWS SNS**, or **PagerDuty** for modern alerting.

✅ **Example Email:**

```
Subject: ALERT: CPU High on webserver-1
Body: High CPU usage detected: 95%
```

---

## 🧰 How to Extend (Production Enhancements)

* Send alerts to **Slack/Teams** via webhooks
* Push metrics to **Prometheus Pushgateway** for visualization
* Include **hostname and IP** in the alert message
* Generate a **daily summary report** from the log file

---

## 💬 Interview-Ready Explanation

> “Before we had centralized monitoring in place, I wrote a lightweight shell script to monitor CPU, memory, and disk usage on EC2 servers.
> It runs every 5 minutes via cron, checks metrics using `top`, `free`, and `df`, and logs them with timestamps.
> If any threshold is exceeded, it sends an email alert to the admin.
> This helped us proactively detect high load or low disk space before it caused downtime.”

---

## 🎯 Common Interview Follow-Up Q&A

### 🧩 Q1: Why use `top`, `free`, and `df` instead of other tools?

> Because they are **lightweight**, available by default on all Linux servers, and don’t require installing external dependencies.

---

### 🧩 Q2: How would you handle multiple servers?

> I’d deploy this script using **Ansible**, and centralize the logs using **CloudWatch** or **ELK Stack** for unified visibility.

---

### 🧩 Q3: How to avoid spam alerts?

> You can track previous states and send alerts only if an issue persists for multiple consecutive checks (e.g., 3 cycles in a row).

---

## ✅ Impact

> “This script helped our team catch resource exhaustion issues early.
> For example, once a deployment filled the root volume — the script alerted us immediately, and we cleaned logs before the server crashed.”

---

## 📂 Folder Structure Example

```
/opt/
 ├── scripts/
 │    └── resource_monitor.sh
 ├── logs/
 │    └── resource_monitor.log
```

---

## 🧠 Key Benefits

* Lightweight, dependency-free monitoring
* Real-time alerting via email or webhook
* Easy to extend for Slack or Prometheus integration
* Simple to deploy via cron or Ansible
* Great for pre-observability or small-scale setups

---

**Author:** *Rupesh Kotal*
**Category:** *DevOps Automation Scripts (Linux / Shell)*

```

---

Would you like me to now combine **Automation #1 – #5** into a single **GitHub-ready repository README.md**  
with an index (like “Automation #1: Log Rotation”, “Automation #2: EC2 Snapshot”, etc.) and clean navigation links for portfolio use?
```
