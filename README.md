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


![image_alt]()












