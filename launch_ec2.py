import boto3

def launch_ec2_instance():
    # Initialize the EC2 client
    ec2 = boto3.client('ec2')
    
    # Specify the details for the EC2 instance
    instance_params = {
        'ImageId': 'ami-085ad6ae776d8f09c',  # Replace with your desired AMI ID
        'InstanceType': 't2.micro',          # Replace with your desired instance type
        'MinCount': 3,
        'MaxCount': 3,
        'TagSpecifications': [
            {
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Environment', 'Value': 'Dev'},
                    {'Key': 'Name', 'Value': 'MyDevInstance'},
                    # Add more tags if needed
                ]
            }
        ],
        # Optional: Specify a key pair for SSH access
        'KeyName': 'ashleyKeypair',     # Replace with your key pair name
        # Optional: Specify a security group
        'SecurityGroupIds': ['sg-03930ca1462264838'],  # Replace with your security group ID
        # Optional: Specify a subnet
        'SubnetId': 'subnet-0a220b62a7bfcf628',       # Replace with your subnet ID
    }
    
    try:
        # Launch the instance
        response = ec2.run_instances(**instance_params)
        
        # Extract the instance ID
        instance_id = response['Instances'][0]['InstanceId']
        print(f"Launched EC2 instance with ID: {instance_id}")
        
        # Optionally, wait for the instance to be in the 'running' state
        waiter = ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])
        print(f"Instance {instance_id} is now running.")
        
        return instance_id
    except Exception as e:
        print(f"Error launching EC2 instance: {e}")
        raise e

if __name__ == "__main__":
    launch_ec2_instance()