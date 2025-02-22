import boto3

def get_active_resource_regions():
    """Fetch AWS regions where the customer has active EC2 instances."""
    ec2_client = boto3.client("ec2")
    regions = [region["RegionName"] for region in ec2_client.describe_regions()["Regions"]]

    active_regions = set()
    for region in regions:
        print(f"🔄 Checking region: {region}...")  # Debugging

        ec2 = boto3.client("ec2", region_name=region)
        try:
            instances = ec2.describe_instances()
            if instances["Reservations"]:
                active_regions.add(region)
                print(f"✅ Active resources found in {region}")
        except Exception as e:
            print(f"⚠️ Skipping {region}: {e}")

    return active_regions

def main():
    active_regions = get_active_resource_regions()
    print("\n✅ Customer is using resources in these regions:", active_regions)

if __name__ == "__main__":
    main()

