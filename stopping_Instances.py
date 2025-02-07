import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    sns = boto3.client('sns')
    
    # Specify the tag key and value
    tag_key = 'Environment'
    tag_value = 'Dev'
    
    # Find instances with the specified tag
    response = ec2.describe_instances(
        Filters=[
            {'Name': f'tag:{tag_key}', 'Values': [tag_value]},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )
    
    instances_to_stop = []
    
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances_to_stop.append(instance['InstanceId'])
    
    if instances_to_stop:
        # Stop the instances
        ec2.stop_instances(InstanceIds=instances_to_stop)
        print(f"Stopped instances: {instances_to_stop}")
        
        # Send notification
        sns_topic_arn = 'arn:aws:sns:us-east-1:664418964175:InstanceStopNotification'
        message = f"The following instances with tag {tag_key}={tag_value} were stopped: {instances_to_stop}"
        sns.publish(TopicArn=sns_topic_arn, Message=message)
        print(f"Notification sent: {message}")
    else:
        print("No instances to stop.")
    
    return {
        'statusCode': 200,
        'body': 'Lambda execution completed.'
    }