# AWS CLI Tool

A simple and reusable AWS CLI tool for managing **EC2 instances**, **SQS queues and messages**, and **CloudWatch logs**.

---

## Features
1. **Manage EC2 Instances**:
   - List, start, stop, and terminate EC2 instances.

2. **Manage SQS Queues**:
   - List, create, send messages, and receive/delete messages.
   - Supports bulk messages with customizable `template.json`.

3. **CloudWatch Logs**:
   - List log groups and streams, and retrieve log events.

---

## Setup Instructions

### Prerequisites
- Python 3.9+ installed.
- AWS credentials with permissions for EC2, SQS, and CloudWatch Logs.
- `pip` installed for managing Python dependencies.

### Installation Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/aws-cli-tool.git
   cd aws-cli-tool
   ```
2. Run the setup script:
    ```bash
    chmod +x setup.sh
    bash setup.sh
    ```
3. Follow the prompts to configure your .env file or create one manually:
   ```bash
    AWS_ACCESS_KEY_ID=your_access_key_id
    AWS_SECRET_ACCESS_KEY=your_secret_access_key
    AWS_DEFAULT_REGION=us-east-1
   ```
4. (Optional) Register the CLI globally:

  - If you chose to register during setup, use the alias awscli to run commands.



## Usage

You can run the CLI using either the alias:
```bash
awscli <command>
```

Or directly invoke the script:
```bash
python3 aws_cli_tool.py <command>
```

## Available Commands

### EC2 Commands

* **List EC2 Instances**
  ```bash
  awscli ec2 list
  ```

* **Start an EC2 Instance**
  ```bash
  awscli ec2 start --instance-id <instance_id>
  ```

* **Stop an EC2 Instance**
  ```bash
  awscli ec2 stop --instance-id <instance_id>
  ```

* **Terminate an EC2 Instance**
  ```bash
  awscli ec2 terminate --instance-id <instance_id>
  ```

### SQS Commands

* **List SQS Queues**
  ```bash
  awscli sqs list
  ```

* **Create an SQS Queue**
  ```bash
  awscli sqs create --name <queue_name> [--fifo]
  ```

* **Send a Message**
  ```bash
  awscli sqs send --queue-url <queue_url> --template-file template.json [--dynamic-values key1=value1,key2=value2]
  ```

* **Send Bulk Messages**
  ```bash
  awscli sqs send-bulk --queue-url <queue_url> --template-file template.json [--dynamic-values key1=value1,key2=value2]
  ```

* **Receive Messages**
  ```bash
  awscli sqs receive --queue-url <queue_url> [--max-messages <number>]
  ```

* **Delete a Message**
  ```bash
  awscli sqs delete --queue-url <queue_url> --receipt-handle <receipt_handle>
  ```

### CloudWatch Logs Commands

* **List Log Groups**
  ```bash
  awscli logs list-groups
  ```

* **List Log Streams in a Group**
  ```bash
  awscli logs list-streams --log-group-name <log_group_name>
  ```

* **Get Log Events from a Stream**
  ```bash
  awscli logs get-events --log-group-name <log_group_name> --log-stream-name <log_stream_name> [--start-time <timestamp>] [--end-time <timestamp>]
  ```

## SQS Message Templates

### Template Format
Create a `template.json` file to define the structure of your SQS messages. You can include placeholders for dynamic values:

```json
{
  "messages": [
    {
      "field1": "{{dynamic_value_1}}",
      "field2": "{{dynamic_value_2}}",
      "uuid": "{{uuid}}",
      "timestamp": "{{timestamp}}"
    }
  ]
}
```

### Available Placeholders
* `{{uuid}}`: Automatically generates a unique ID
* `{{timestamp}}`: Inserts the current timestamp
* Custom placeholders: Define your own using `--dynamic-values`

## Troubleshooting

### Missing AWS Credentials
Ensure the `.env` file exists and contains valid AWS credentials.

### Python Version Requirements
* Check your Python version:
  ```bash
  python3 --version
  ```
* Python 3.9 or higher is required

### Dependency Installation Issues
If dependency installation fails:
1. Verify pip is installed correctly
2. Try manual installation:
   ```bash
   pip install -r requirements.txt
   ```

### Template Errors
* Verify JSON syntax in `template.json`
* Ensure placeholder names in template match the keys provided in `--dynamic-values`
* Check for proper formatting and closing brackets
