# EC2-Dev-Environment-Shutdown-Automation-Using-Python


"AWS Event-driven Architecture"

# Technical Architecture

![image_alt]()


## Project Overview

This project automates the shutdown of AWS EC2 instances tagged with `environment=Dev` to save costs. It utilizes AWS Lambda, EventBridge, and SNS to identify, stop, and notify administrators about stopped instances.

## Project Objectives

The objective of this project is to automate the shutdown of AWS EC2 instances tagged with `environment=Dev` to optimize costs and resource management. Using an EventBridge rule, the system triggers an AWS Lambda (Python) function on a scheduled basis to identify and stop running instances. Additionally, an SNS notification alerts administrators about the stopped instances, ensuring transparency. This serverless, event-driven approach enhances efficiency, reduces unnecessary cloud expenses, and eliminates manual intervention.

## Prerequisites

1.AWS Account with an IAM User

2.Basic knowledge of the Python Programming Language

3.Basic knowledge and use of an Interactive Development Environment(Visual Code Studio)


## Use Case

You work at a DevOps Team at Up The Chelsea Corp and they prioritize cost optimization by automatically shutting down non-production EC2 instances outside work hours, reducing unnecessary cloud expenses. It enhances resource management by ensuring Dev instances do not run unattended, improving efficiency. Additionally, it supports security compliance by preventing prolonged exposure of development environments. This automation also integrates well into DevOps workflows, enabling efficient environment lifecycle management while ensuring timely cleanup of unused resources.


## Step 1:Create an SNS Topic for Notifications

1.1.Nativage to the Amazon SNS console.

Create a new SNS topic (e.g., InstanceStopNotification).

![image_alt](https://github.com/Tatenda-Prince/EC2-Dev-Environment-Shutdown-Automation-Using-Python/blob/c6e364bd496830caa7f5cf3bbbb39a8b6e90a2d3/img/Screenshot%202025-02-07%20171937.png)

1.2.Subscribe your email or other endpoints to the topic to receive notifications.

![image_alt](https://github.com/Tatenda-Prince/EC2-Dev-Environment-Shutdown-Automation-Using-Python/blob/984e1090cbb9e484da98f7d840499c5fb9e8c691/img/Screenshot%202025-02-07%20172117.png)



## Step 2: Set up Lambda Function and IAM Role

Navigate to AWS Lambda in the AWS Management Console and click “Create Function”.

2.1.Select “Author from scratch”, name the function, then choose Python 3.7 or greater Runtime.

![image_alt](https://github.com/Tatenda-Prince/EC2-Dev-Environment-Shutdown-Automation-Using-Python/blob/6dd3cc0fad7919d180399ead0cdadbded389f569/img/Screenshot%202025-02-07%20172231.png)

2.2.Under Permissions, create a new IAM role with the following permissions:

`ec2:DescribeInstances`

`ec2:StopInstances`

`sns:Publish`

2.3.Click “Create policy”, then select the “JSON” table to edit the policy. Copy and paste the JSON policy below in the policy box, then click “Next:Tags”.
create a role with this policy attached



```language

json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:StopInstances"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "sns:Publish",
      "Resource": "*"
    }
  ]
}

```


2.4.Head back to the Lambda’s “Create function” window. Refresh the existing roles, select the role previously created, then click “Create Function”.


![image_alt](https://github.com/Tatenda-Prince/EC2-Dev-Environment-Shutdown-Automation-Using-Python/blob/235b79137302b284942be6b9b597b365a679a3f1/img/Screenshot%202025-02-07%20172248.png)


## Step 3: Write the Lambda Function Code

3.1.This AWS Lambda function is designed to stop EC2 instances that are tagged with "Environment=Dev" and are currently running. It uses the EC2 and SNS clients from the boto3 library to find instances with this tag and state. If any matching instances are found, the function stops them and sends a notification via SNS with the list of stopped instances. If no such instances are found, it simply prints a message indicating that no instances were stopped. The function returns a status code and a completion message upon execution.


Replace the default code with the following Python script:


```python

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
```


3.2.Next, we will click “Deploy” to deploy the function’s code to the Lambda service, then click “Test” to test out the function based on a test case.
For “Test event action”, select “Create a new event”, then name the event. We can use the JSON code below to test our Lambda function.

Click “Save” to save the Test event.


![image_alt](https://github.com/Tatenda-Prince/EC2-Dev-Environment-Shutdown-Automation-Using-Python/blob/35a4d50e1e67b9b75a5b4cc5f7b84661eca8b152/img/Screenshot%202025-02-07%20172711.png)



3.3.We can now test our function by clicking ‘Test”. A “success” response, along with other details from the function execution in the function logs should display in the “Executing results” tab.


![image_alt](https://github.com/Tatenda-Prince/EC2-Dev-Environment-Shutdown-Automation-Using-Python/blob/f91ea8aec14b58764e746ee2a25d012a3ae83a82/img/Screenshot%202025-02-07%20172834.png)


## Step 4: Create an EventBridge Rule

4.1.Navigate to EventBridge, select “EventBridge Schedule” then click “Create Rule”.
Name and describe (optional) your schedule and set “Schedule group” to default.

![image_alt](https://github.com/Tatenda-Prince/EC2-Dev-Environment-Shutdown-Automation-Using-Python/blob/d3dfd822550845f50def8eab2e21abb64f9fb6b5/img/Screenshot%202025-02-07%20173122.png)


4.2.For “Schedule pattern” select “Recurring schedule” since we want the Lambda function to execute at 7pm every working day.
Select “Cron-based schedule” and use the cron expression as seen below, then click “Next”.

![image_alt]()

4.3.Select “AWS Lambda — Invoke”, choose your Lambda function, then click “Next”.

![image_alt]()


4.4.Continue to the “Review and create schedule”, then click “Create schedule”.
You should now be able to see the new Schedule just created in EventBridge.

![image_alt]()


Now that we’ve scheduled the execution of our Lambda function, we can proceed to Step 5 — Automating the launching of Dev EC2 Instances.
















