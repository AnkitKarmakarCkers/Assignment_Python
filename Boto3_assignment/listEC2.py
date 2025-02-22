import boto3
import csv
import botocore.exceptions

def list_instance_types():
    ec2_client = boto3.client("ec2")
    regions = [region["RegionName"] for region in ec2_client.describe_regions()["Regions"]]

    instance_data = []
    for region in regions:
        print(f"Checking region: {region}")  # Debugging output
        ec2_client = boto3.client("ec2", region_name=region)

        try:
            paginator = ec2_client.get_paginator("describe_instance_type_offerings")
            response_iterator = paginator.paginate(
                LocationType='region',
                PaginationConfig={'MaxItems': 100}  # Limits to avoid hanging
            )

            instance_types = set()
            for page in response_iterator:
                for instance in page["InstanceTypeOfferings"]:
                    instance_types.add(instance["InstanceType"])

            for instance_type in instance_types:
                instance_data.append([region, instance_type])

        except botocore.exceptions.EndpointConnectionError:
            print(f"⚠️  Network issue: Could not connect to region {region}")
        except botocore.exceptions.ClientError as e:
            print(f"❌ AWS Error in region {region}: {e}")
        except Exception as e:
            print(f"❗ Unexpected error in {region}: {e}")

    with open("ec2_instance_types.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["region", "instance_type"])
        writer.writerows(instance_data)

    print("✅ CSV file 'ec2_instance_types.csv' created successfully.")

if __name__ == "__main__":
    list_instance_types()
