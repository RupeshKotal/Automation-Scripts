#!/usr/bin/env python3
import boto3
from datetime import datetime, timedelta

# Initialize clients
ec2 = boto3.client('ec2', region_name='ap-south-1')
cloudwatch = boto3.client('cloudwatch', region_name='ap-south-1')

# Define threshold and time range
CPU_THRESHOLD = 5     # % CPU utilization
DAYS = 2              # Days to check
end_time = datetime.utcnow()
start_time = end_time - timedelta(days=DAYS)

def get_cpu_utilization(instance_id):
    """Fetch average CPU usage from CloudWatch"""
    metrics = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,
        Statistics=['Average']
    )
    datapoints = metrics.get('Datapoints', [])
    if datapoints:
        avg_cpu = sum(dp['Average'] for dp in datapoints) / len(datapoints)
        return round(avg_cpu, 2)
    return 0

def main():
    print("🔍 Checking for idle EC2 instances...")
    instances = ec2.describe_instances(Filters=[
        {'Name': 'instance-state-name', 'Values': ['running']}
    ])

    idle_instances = []

    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            name_tag = next((t['Value'] for t in instance.get('Tags', []) if t['Key'] == 'Name'), "NoName")

            cpu_usage = get_cpu_utilization(instance_id)
            print(f"{instance_id} ({name_tag}) → Avg CPU: {cpu_usage}%")

            if cpu_usage < CPU_THRESHOLD:
                idle_instances.append(instance_id)

    if idle_instances:
        print(f"🛑 Stopping idle instances: {idle_instances}")
        ec2.stop_instances(InstanceIds=idle_instances)
    else:
        print("✅ No idle instances found.")

if __name__ == "__main__":
    main()
