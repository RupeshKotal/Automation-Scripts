Here’s your entire content formatted neatly as a **README.md** file:

---

````markdown
# 🧠 Automation #1: Log Rotation & Archival Script (Shell)

## 🧾 Problem

Application logs (like `/var/log/app.log`) grow daily and can fill up server storage, potentially causing downtime or performance issues.  
Manual cleanup isn’t scalable.

---

## ⚙️ Goal

Automate **log rotation**, **compression**, **cleanup**, and **alerting**.

---

## 🧩 Shell Script: `log_rotate.sh`

```bash
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
````

---

## 🕒 Schedule via Cron

Add this entry to your cron job to run the script every midnight:

```bash
0 0 * * * /opt/scripts/log_rotate.sh
```

---

## 💬 Interview-Ready Explanation

> “In one of my projects, we had an issue where application logs were growing rapidly and consuming disk space.
> To handle this, I wrote a simple log rotation script using Bash.
> It compresses all `.log` files every midnight, moves them to a backup folder, and deletes files older than 7 days.
> I also added logging to track the rotation process and scheduled it via cron.
> This reduced disk utilization issues and improved our overall log management process.”

---

## 🎯 Common Follow-Up Q&A

### 🧩 Q1: How did you monitor if the script was failing?

> I logged all actions and errors into a `backup.log` file and also configured a cron email alert for failures.
> Later, I integrated it with a Slack webhook for notifications.

---

### 🧩 Q2: How would you scale this across multiple servers?

> I’d package it as a lightweight script deployed via **Ansible** or **Jenkins**,
> or move to a centralized solution like **logrotate** or **CloudWatch Logs** for consistent rotation across all servers.

---

### 🧩 Q3: Why not use logrotate utility directly?

> For critical logs with **custom naming conventions** or **non-standard retention policies**,
> I wanted more flexibility with my own script.
> But generally, yes — `logrotate` is the preferred and more scalable approach in large environments.

---

## 📂 Folder Structure Example

```
/opt/
 ├── scripts/
 │    └── log_rotate.sh
 ├── utxapp/
 │    ├── logs/
 │    │     ├── app.log
 │    │     └── error.log
 │    └── backup/
 │          ├── app.log-2025-11-05.gz
 │          ├── error.log-2025-11-05.gz
 │          └── backup.log
```

---

## ✅ Key Benefits

* Prevents log files from consuming full disk space
* Automates archival and cleanup
* Simple to monitor and schedule via cron
* Easily extensible for multi-server environments
* Reduces manual effort and improves observability

---

**Author:** *Rupesh Kotal*
**Category:** *DevOps Automation Scripts (Shell / Linux)*

```

---

Would you like me to add a small “📊 Metrics or Monitoring Integration” section showing how to send alerts (like via Slack or email) when the rotation fails? It would make your README more production-grade.
```
