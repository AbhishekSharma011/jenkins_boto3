import boto3
import time

# Initialize Boto3 clients
ec2 = boto3.client('ec2', region_name='us-east-1')

# Variables
key_name = "jenkins-key"  # Existing key pair
security_group_id = "sg-009e7db7aaed1f565"  # Existing security group ID
ami_id = "ami-04b4f1a9cf54c11d0"  # AMI ID
instance_type = "t2.micro"  # Instance type
setup_script_path = "setup_jenkins.sh"  # Path to the setup script
ssh_user = "ubuntu"  # SSH user
ssh_key_path = "jenkins-key.pem"  # Path to the private key file

# Read the setup script
with open(setup_script_path, "r") as file:
    setup_script = file.read()

# Launch EC2 instance
response = ec2.run_instances(
    ImageId=ami_id,
    InstanceType=instance_type,
    KeyName=key_name,
    SecurityGroupIds=[security_group_id],
    MinCount=1,
    MaxCount=1,
    TagSpecifications=[
        {
            "ResourceType": "instance",
            "Tags": [
                {"Key": "Name", "Value": "jenkins"},
            ],
        },
    ],
)

# Get instance ID
instance_id = response["Instances"][0]["InstanceId"]
print(f"Instance {instance_id} is launching...")

# Wait for the instance to be running
waiter = ec2.get_waiter("instance_running")
waiter.wait(InstanceIds=[instance_id])

# Get public IP address
instance = ec2.describe_instances(InstanceIds=[instance_id])
public_ip = instance["Reservations"][0]["Instances"][0]["PublicIpAddress"]
print(f"Instance {instance_id} is running. Public IP: {public_ip}")

# Wait for SSH to be available
time.sleep(60)  # Adjust this delay as needed

# Copy and execute the setup script using SSH
import paramiko

# Connect to the instance
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(public_ip, username=ssh_user, key_filename=ssh_key_path)

# Copy the setup script to the instance
sftp = ssh.open_sftp()
sftp.put(setup_script_path, "/tmp/setup-jenkins.sh")
sftp.close()

# Execute the setup script
commands = [
    "chmod +x /tmp/setup-jenkins.sh",
    "sudo /tmp/setup-jenkins.sh",
]

for command in commands:
    stdin, stdout, stderr = ssh.exec_command(command)
    print(stdout.read().decode())
    print(stderr.read().decode())

# Close SSH connection
ssh.close()

print("Jenkins setup complete!")
print(f"Access Jenkins at http://{public_ip}:8080")