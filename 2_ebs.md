Here’s your **Automation #2** neatly formatted as a professional `README.md` entry (in the same style as Automation #1):

---

````markdown
# 🧩 Automation #2: EC2 Snapshot Backup Script (Python)

## 🧾 Problem

In many projects, EBS snapshots were taken **manually** for backups — a process that’s **error-prone** and **not scalable**.  
To automate this, I built a Python-based solution that creates and cleans up EC2 EBS snapshots daily.

---

## ⚙️ Code Snippet: `ec2_snapshot_backup.py`

```python
#!/usr/bin/env python3
import boto3
from datetime import datetime, timedelta

ec2 = boto3.client('ec2', region_name='ap-south-1')

# Retention period (in days)
retention_days = 7
today = datetime.now().strftime('%Y-%m-%d')

def lambda_handler(event=None, context=None):
    # 1️⃣ Get all instances with Backup=True tag
    instances = ec2.describe_instances(
        Filters=[{'Name': 'tag:Backup', 'Values': ['True']}]
    )

    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            print(f"Creating snapshot for {instance_id}")
            
            # 2️⃣ Create snapshot for each volume
            for vol in instance['BlockDeviceMappings']:
                vol_id = vol['Ebs']['VolumeId']
                desc = f"Backup-{instance_id}-{today}"
                snapshot = ec2.create_snapshot(VolumeId=vol_id, Description=desc)
                
                # Add tags
                ec2.create_tags(Resources=[snapshot['SnapshotId']], Tags=[
                    {'Key': 'Name', 'Value': desc},
                    {'Key': 'CreatedOn', 'Value': today}
                ])

    # 3️⃣ Delete old snapshots
    delete_old_snapshots()

def delete_old_snapshots():
    old_date = datetime.now() - timedelta(days=retention_days)
    snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']

    for snap in snapshots:
        if 'StartTime' in snap and snap['StartTime'].date() < old_date.date():
            print(f"Deleting old snapshot: {snap['SnapshotId']}")
            ec2.delete_snapshot(SnapshotId=snap['SnapshotId'])

if __name__ == "__main__":
    lambda_handler()
````

---

## 💡 How It Works

1. **Fetch EC2 instances** that have a tag `Backup=True`
2. **Iterate** through all attached EBS volumes and **create snapshots**
3. **Tag snapshots** with `Name` and `CreatedOn` for traceability
4. **Delete old snapshots** older than 7 days to save cost

You can run this script in two ways:

* As a **CronJob** on an EC2 instance
* As an **AWS Lambda function** triggered by a **CloudWatch Event Rule** (daily at midnight)

---

## 💬 Interview-Ready Explanation

> “I built a Python automation to manage EC2 EBS backups automatically.
> It uses the boto3 SDK to find all instances tagged with Backup=True, create snapshots for each attached EBS volume, and tag them with the creation date.
> Then it checks for old snapshots beyond 7 days and deletes them to reduce cost.
> We scheduled it via CloudWatch Event Rules to run daily at midnight.
> This completely removed manual intervention and ensured consistent backup hygiene.”

---

## 🎯 Common Interview Follow-Ups

### 🧩 Q1: Why did you use tags like `Backup=True`?

> To **selectively back up** only critical instances instead of all EC2s — this provides better control and avoids unnecessary storage costs.

---

### 🧩 Q2: How did you handle permissions?

> The Lambda/EC2 IAM Role included:
>
> * `ec2:DescribeInstances`
> * `ec2:CreateSnapshot`
> * `ec2:DeleteSnapshot`
> * `ec2:CreateTags`
>   These were the minimum permissions needed for the script to run successfully.

---

### 🧩 Q3: How did you monitor success or failure?

> I logged actions to **CloudWatch Logs** and set up a **CloudWatch Alarm** to trigger alerts if the number of snapshots didn’t increase overnight.

---

### 🧩 Q4: Why use Python instead of AWS Backup service?

> AWS Backup works well but can be **costlier** and less flexible for **custom tagging**, **naming**, or **retention policies**.
> Python with boto3 gave full control and easy integration with Jenkins or cron.

---

## ✅ Impact

> “Before automation, backups took 30–40 mins of manual effort daily.
> After this automation, it runs automatically at midnight and maintains a 7-day retention cycle — saving both **time** and **AWS storage cost**.”

---

## 📂 Example Folder Structure

```
/opt/
 ├── scripts/
 │    └── ec2_snapshot_backup.py
 ├── logs/
 │    └── snapshot_backup.log
```

---

## 🧠 Key Benefits

* Fully automated daily EBS snapshot management
* Ensures data safety with configurable retention
* Lightweight and serverless using AWS Lambda
* Easily scalable via tags and IAM roles
* Reduces manual work and operational risk

---

**Author:** *Rupesh Kotal*
**Category:** *DevOps Automation Scripts (AWS / Python)*

```

---

Would you like me to merge **Automation #1 and #2** into a single `README.md` file (as part of a “DevOps Automation Scripts Collection”)?  
It would look like a professional open-source repo format — with a TOC, description, and sections for each automation.
```
