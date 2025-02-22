import boto3
import csv

iam_client = boto3.client('iam')
ec2_client = boto3.client('ec2')

def get_admin_roles():
    roles = iam_client.list_roles()["Roles"]
    admin_roles = []
    
    for role in roles:
        role_name = role["RoleName"]
        policies = iam_client.list_attached_role_policies(RoleName=role_name)["AttachedPolicies"]
        
        for policy in policies:
            if policy["PolicyName"] == "AdministratorAccess":
                admin_roles.append([role_name, policy["PolicyName"]])
    
    with open("iam_admin_roles.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["IAMRoleName", "PolicyName"])
        writer.writerows(admin_roles)

def get_mfa_status():
    users = iam_client.list_users()["Users"]
    user_mfa_status = []
    
    for user in users:
        username = user["UserName"]
        mfa_enabled = "True" if iam_client.list_mfa_devices(UserName=username)["MFADevices"] else "False"
        user_mfa_status.append([username, mfa_enabled])
    
    with open("iam_mfa_status.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["IAMUserName", "MFAEnabled"])
        writer.writerows(user_mfa_status)

def get_public_security_groups():
    security_groups = ec2_client.describe_security_groups()["SecurityGroups"]
    insecure_sgs = []
    
    for sg in security_groups:
        sg_name = sg["GroupName"]
        
        for rule in sg["IpPermissions"]:
            port = rule.get("FromPort", "N/A")
            for ip_range in rule.get("IpRanges", []):
                if ip_range["CidrIp"] == "0.0.0.0/0" and port in [22, 80, 443]:
                    insecure_sgs.append([sg_name, port, ip_range["CidrIp"]])
    
    with open("insecure_security_groups.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["SGName", "Port", "AllowedIP"])
        writer.writerows(insecure_sgs)

def get_unused_key_pairs():
    key_pairs = {kp["KeyName"] for kp in ec2_client.describe_key_pairs()["KeyPairs"]}
    used_keys = set()
    
    for res in ec2_client.describe_instances()["Reservations"]:
        for instance in res["Instances"]:
            if "KeyName" in instance:
                used_keys.add(instance["KeyName"])
    
    unused_keys = key_pairs - used_keys
    
    with open("unused_key_pairs.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["UnusedKeyName"])
        writer.writerows([[key] for key in unused_keys])

if __name__ == "__main__":
    get_admin_roles()
    get_mfa_status()
    get_public_security_groups()
    get_unused_key_pairs()
    print("Security reports generated successfully.")
