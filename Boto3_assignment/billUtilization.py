import boto3
import csv
from datetime import datetime, timedelta

ec2_client = boto3.client('ec2')
rds_client = boto3.client('rds')
lambda_client = boto3.client('lambda')
s3_client = boto3.client('s3')
cloudwatch_client = boto3.client('cloudwatch')

def get_low_utilization_ec2():
    instances = ec2_client.describe_instances()["Reservations"]
    low_util_instances = []
    
    for res in instances:
        for instance in res["Instances"]:
            instance_id = instance["InstanceId"]
            stats = cloudwatch_client.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                StartTime=datetime.utcnow() - timedelta(days=30),
                EndTime=datetime.utcnow(),
                Period=86400,
                Statistics=['Average']
            )
            avg_cpu = sum(dp['Average'] for dp in stats['Datapoints']) / len(stats['Datapoints']) if stats['Datapoints'] else 0
            if avg_cpu < 10:
                low_util_instances.append([instance_id, avg_cpu])
    
    with open("low_util_ec2.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["InstanceId", "AvgCPUUtilization"])
        writer.writerows(low_util_instances)

def get_idle_rds_instances():
    instances = rds_client.describe_db_instances()["DBInstances"]
    idle_rds = []
    
    for instance in instances:
        instance_id = instance["DBInstanceIdentifier"]
        stats = cloudwatch_client.get_metric_statistics(
            Namespace='AWS/RDS',
            MetricName='DatabaseConnections',
            Dimensions=[{'Name': 'DBInstanceIdentifier', 'Value': instance_id}],
            StartTime=datetime.utcnow() - timedelta(days=7),
            EndTime=datetime.utcnow(),
            Period=86400,
            Statistics=['Sum']
        )
        total_connections = sum(dp['Sum'] for dp in stats['Datapoints']) if stats['Datapoints'] else 0
        if total_connections == 0:
            idle_rds.append([instance_id])
    
    with open("idle_rds_instances.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["DBInstanceIdentifier"])
        writer.writerows(idle_rds)

def get_unused_lambda_functions():
    functions = lambda_client.list_functions()["Functions"]
    unused_lambdas = []
    
    for function in functions:
        function_name = function["FunctionName"]
        stats = cloudwatch_client.get_metric_statistics(
            Namespace='AWS/Lambda',
            MetricName='Invocations',
            Dimensions=[{'Name': 'FunctionName', 'Value': function_name}],
            StartTime=datetime.utcnow() - timedelta(days=30),
            EndTime=datetime.utcnow(),
            Period=86400,
            Statistics=['Sum']
        )
        total_invocations = sum(dp['Sum'] for dp in stats['Datapoints']) if stats['Datapoints'] else 0
        if total_invocations == 0:
            unused_lambdas.append([function_name])
    
    with open("unused_lambda_functions.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["FunctionName"])
        writer.writerows(unused_lambdas)

def get_unused_s3_buckets():
    buckets = s3_client.list_buckets()["Buckets"]
    unused_buckets = []
    
    for bucket in buckets:
        bucket_name = bucket["Name"]
        objects = s3_client.list_objects_v2(Bucket=bucket_name)
        if "Contents" not in objects:
            unused_buckets.append([bucket_name])
    
    with open("unused_s3_buckets.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["BucketName"])
        writer.writerows(unused_buckets)

if __name__ == "__main__":
    get_low_utilization_ec2()
    get_idle_rds_instances()
    get_unused_lambda_functions()
    get_unused_s3_buckets()
    print("Cost optimization reports generated successfully.")
