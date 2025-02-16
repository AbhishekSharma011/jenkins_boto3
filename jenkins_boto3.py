import boto3
import paramiko
import time

# Initialize Boto3 EC2 client
ec2 = boto3.resource('ec2', region_name='us-east-1')


# Step 1: Create a Key Pair
def create_key_pair(key_name):
    key_pair = ec2.create_key_pair(KeyName=key_name)
    private_key = key_pair.key_material

    # Save the private key to a file
    with open(f"{key_name}.pem", 'w') as file:
        file.write(private_key)

    print(f"Key pair {key_name} created and saved as {key_name}.pem")


# Step 2: Create a Security Group
def create_security_group(group_name, description):
    security_group = ec2.create_security_group(GroupName=group_name, Description=description)

    # Add ingress rules (SSH and HTTP)
    security_group.authorize_ingress(
        IpPermissions=[
            {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 8080, 'ToPort': 8080, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ]
    )

    print(f"Security group {group_name} created with SSH and HTTP rules.")
    return security_group.id


# Step 3: Launch EC2 Instance
def launch_ec2_instance(ami_id, instance_type, key_name, security_group_id):
    instance = ec2.create_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        KeyName=key_name,
        SecurityGroupIds=[security_group_id],
        MinCount=1,
        MaxCount=1
    )[0]

    # Wait for the instance to start
    instance.wait_until_running()
    instance.reload()

    print(f"EC2 Instance {instance.id} launched with public IP {instance.public_ip_address}")
    return instance.public_ip_address


# Step 4: SSH into EC2 and setup Jenkins (using Paramiko)
def setup_jenkins(ip_address, key_file, user='ec2-user'):
    # Initialize SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Read the private key
    private_key = paramiko.RSAKey.from_private_key_file(key_file)

    # Connect to the EC2 instance
    ssh.connect(hostname=ip_address, username=user, pkey=private_key)

    # Execute commands to setup Jenkins
    commands = [
        'sudo yum update -y',
        'sudo yum install java-11-openjdk-devel -y',
        'wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat/jenkins.repo',
        'rpm --import https://pkg.jenkins.io/redhat/jenkins.io.key',
        'sudo yum install jenkins -y',
        'sudo systemctl start jenkins',
        'sudo systemctl enable jenkins'
    ]

    for command in commands:
        stdin, stdout, stderr = ssh.exec_command(command)
        print(stdout.read().decode())
        print(stderr.read().decode())

    print("Jenkins setup completed.")
    ssh.close()


# Putting it all together
if __name__ == "__main__":
    key_name = "jenkins-key"
    security_group_name = "jenkins-sg"
    ami_id = "ami-04b4f1a9cf54c11d0"  # Example AMI for Jenkins
    instance_type = "t2.micro"

    create_key_pair(key_name)
    sg_id = create_security_group(security_group_name, "Jenkins security group")
    ip_address = launch_ec2_instance(ami_id, instance_type, key_name, sg_id)

    time.sleep(60)  # Wait for the instance to be fully ready before SSH

    setup_jenkins(ip_address, f"{key_name}.pem")
