# Jenkins Infrastructure Setup on AWS using Python (Boto3)

This repository contains a Python script to automate the process of launching an EC2 instance on AWS, installing Jenkins, and configuring it using an SSH connection. The script utilizes Boto3 to interact with AWS and Paramiko for remote server setup.

## Features

Launches an EC2 instance using a specified AMI and instance type.

Attaches an existing Security Group and Key Pair.

Automatically installs and configures Jenkins using a setup script.

Provides access to Jenkins via the public IP of the instance.

## Prerequisites

Before running the script, ensure you have the following:

Python 3.x installed.

Boto3 and Paramiko libraries installed. You can install them using:

### **pip install boto3 paramiko**

AWS CLI configured with the necessary credentials:

### **aws configure**

An existing EC2 key pair and security group with inbound rules allowing access to ports 8080 (for Jenkins) and 22 (for SSH).

An Ubuntu AMI that supports Jenkins installation (you can modify the AMI ID in the script).

A setup script (setup_jenkins.sh) that installs Jenkins on the EC2 instance.

## How to Use

### Clone the repository:

### **git clone https://github.com/AbhishekSharma011/jenkins_boto3.git**
### **cd jenkins_boto3**

Configure the script: Edit the Python script create_jenkins_infra.py and replace the following variables with your own values:

key_name: Name of your existing EC2 key pair.

security_group_id: ID of your existing security group.

ami_id: The AMI ID for an Ubuntu instance.


instance_type: Instance type (e.g., t2.micro).

setup_script_path: Path to the Jenkins setup script (e.g., setup_jenkins.sh).

ssh_user: SSH username (default for Ubuntu AMIs is ubuntu).

ssh_key_path: Path to the private key file (e.g., jenkins-key.pem).

Run the Python script: Execute the script to launch an EC2 instance and set up Jenkins:

### **python jenkins_boto3.py**

Access Jenkins: Once the script completes, it will display the public IP of the instance. You can access Jenkins via the following URL:

http://< EC2-Instance-Public-IP >:8080

## Files

jenkins_boto3.py: Python script to launch the EC2 instance and configure Jenkins.

setup_jenkins.sh: Shell script for installing and configuring Jenkins on the EC2 instance.

## Cleanup

To terminate the EC2 instance, you can do so manually from the AWS Console or modify the script to include a termination function.

## License

This project is licensed under the MIT License.

Contact
For any questions, feel free to open an issue or reach out to Abhishek Sharma.
