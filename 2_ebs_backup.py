#!/usr/bin/env python3
import boto3
from datetime import datetime, timedelta

ec2 = boto3.client('ec2', region_name='ap-south-1')

# Retention period (in days)
retention_days = 7
today = datetime.now().strftime('%Y-%m-%d')

def lambda_handler(event=None, context=None):
    # 1️⃣ Get all instances with Backup tag
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
