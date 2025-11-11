# Serverless Notification Service

This is a serverless notification system that is highly open to expansion.

The system is completely open to the inclusion of new notification providers. It is possible to integrate new notification providers without the need to make major adjustments to the base code. All you need to do is implement an interface and register it in the settings.

In addition, the notification is parameterized according to the preferences of each user registered in the database.

## ☁️ System overview

![application-schema](/assets/application.svg)

## Tecnologies

### Tools
- Python 3.13
- MongoDB
- AWS S3
- AWS Lambda
- AWS Event Bridge
- AWS SNS
- AWS SQS

### Optional tools
- AWS Secret Manager: Used for provider Google Calendar, what a need for user credentials. The tool is optional as all provider is optional.

### Infra & CI/CD
- AWS
- Terraform
- Github Actions

<details>
    <summary><h2>Details</h2></summary>

### How it works
A scheduler in Event Bridge is configured to periodically (e.g. daily) trigger an event that calls the `notification-publisher` Lambda function.

The `notification-publisher` service is responsible for fetching, filtering, and segregating notifications. It fetches notifications from MongoDB according to the defined filters, processes them, and then sends them to AWS SNS, with one message for each provider chosen by the user. It is possible to configure which providers will be used for a user from the `providers` attribute in the MongoDB database; this is a list of strings containing the names of the providers that will be used; the value of the strings must match the name of the providers registered in the system (`NotificationProviderEnum` enum class).

SNS is a real-time messaging service that allows you to send and receive messages between different AWS services and third parties. In this system, the responsibility is to forward the messages to a queue in AWS SQS. When a new message enters the SQS queue, the `notification-dispatcher` Lambda is automatically triggered.

The `notification-dispatcher` Lambda is responsible for reading the message from the SQS queue and processing it to send a notification to the user using a specific notification provider selected by the user.

By default, the application already has integration with Google Calendar and Whatsapp. However, it is possible to add new notification providers by following the steps below.


### Data Structures (models & MongoDB collections)
For the application to work, the following data structures are used in MongoDB:

#### User:
```python
full_name: str
email: str
phone: str
providers: list[str]
```

#### Event:
```python
title: str
description: str
dt_init: datetime
dt_end: datetime
user: User
```

### Adding new notification providers
To include new providers, changes are only required in the `dispatcher-service` system.

Step by step:
1. Implement the `NotificationProviderI` class,
2. Create a new key for the new provider in the `NotificationProviderEnum` enum
3. Add the new provider in the `load_notification_provider_registry` function.

</details>

<details>
  <summary><h2>How to run</h2></summary>

### Prerequisites
- AWS access key (third party service)
- AWS CLI
- Terraform

### AWS Roles/Policies
- AmazonEventBridgeFullAccess
- AmazonS3FullAccess
- AmazonSNSFullAccess
- AmazonSQSFullAccess
- AWSLambda_FullAccess
- CloudWatchLogsFullAccess
- iam:*

<details>
    <summary><h3>Envs</h3></summary>

#### Lambda - Publisher:
```.env
# Database
DB_USERNAME
DB_PASSWORD
DB_NAME
DB_PORT
DB_URI
DB_URI_ARGS # Opcional

# AWS
SNS_PATH
```

#### Lambda - Dispatcher:
```.env
# API token
WHATSAPP_API_TOKEN
```

#### Pipeline vars/secrets:
```
# Vars
REGION
TFSTATE_BUCKET_NAME

# Secrets
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY

DB_NAME
DB_PASSWORD
DB_PORT
DB_URI
DB_URI_ARGS
DB_USERNAME

WHATSAPP_API_TOKEN
```

#### Terraform envs:
``` .env
TF_LOG
TF_VAR_publisher_source_code_zip
TF_VAR_dispatcher_source_code_zip
TF_VAR_publisher_source_code_lambda_s3_zip_name
TF_VAR_dispatcher_source_code_lambda_s3_zip_name
TF_VAR_region
TF_VAR_tfstate_bucket_name
TF_VAR_whatsapp_api_token
TF_VAR_db_username
TF_VAR_db_password
TF_VAR_db_name
TF_VAR_db_port
TF_VAR_db_uri
TF_VAR_db_uri_args
```
</details>


<details>
  <summary><h3>Implementation step by step</h3></summary>

> **IMPORTANT** \
> Configure all necessary envs (Terraform envs)

#### Build
Generate an application zip along with all dependencies at the same level as the `` src`` directory.
```bash
python -m pip install --upgrade pip
mkdir package
pip install -r requirements.txt -t package/
cp -r src package/
cp lambda_function.py package/

cd package
zip -r "../source_code.zip" . # Remember to assign the same name in the environment variable TF_VAR_code_result_zip
cd ..
```
#### Terraform
1. Create a bucket for the Terraform state file and set its name to the ``TF_VAR_tfstate_bucket_name`` environment variable

2. Configure all environment variables

3. Init
    ```bash
    terraform init \
        -backend-config="bucket=$TF_VAR_tfstate_bucket_name" \
        -backend-config="key=terraform.state" \
        -backend-config="region=$TF_VAR_region"
    ```

4. Valide
    ```terraform
    terraform validate
    ```

5. Plan
    ```terraform
    terraform plan
    ```

6. Apply
    ```terraform
    terraform apply
    ```
</details>

</details>
