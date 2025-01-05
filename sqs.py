import boto3
import typer
import json
import uuid
from datetime import datetime
from config import validate_aws_config

sqs_app = typer.Typer(help="Commands to manage SQS queues and messages.")

# Initialize SQS client
def get_sqs_client():
    return boto3.client("sqs")


@sqs_app.command("list")
def list_queues():
    """
    List all SQS queues.
    """
    validate_aws_config()  
    client = get_sqs_client()
    response = client.list_queues()
    queues = response.get("QueueUrls", [])
    if queues:
        print("SQS Queues:")
        for queue_url in queues:
            print(queue_url)
    else:
        print("No SQS queues found.")


@sqs_app.command("create")
def create_queue(
    name: str,
    fifo: bool = typer.Option(False, help="Create a FIFO queue."),
):
    """
    Create an SQS queue.
    """
    validate_aws_config() 
    client = get_sqs_client()
    attributes = {}
    if fifo:
        name += ".fifo"
        attributes["FifoQueue"] = "true"
        attributes["ContentBasedDeduplication"] = "true"
    response = client.create_queue(QueueName=name, Attributes=attributes)
    print(f"Queue created: {response['QueueUrl']}")


@sqs_app.command("send")
def send_message(queue_url: str, template_file: str, dynamic_values: str = None):
    """
    Send a single message to an SQS queue using a template.json file.
    """
    validate_aws_config() 
    client = get_sqs_client()

    dynamic_values_dict = parse_dynamic_values(dynamic_values)
    messages = process_template(template_file, dynamic_values_dict)


    if messages:
        response = client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(messages[0]),
        )
        print(f"Message sent. ID: {response['MessageId']}")
    else:
        print("No messages to send. Check your template.")


@sqs_app.command("send-bulk")
def send_bulk_messages(queue_url: str, template_file: str, dynamic_values: str = None):
    """
    Send multiple messages to an SQS queue using a template.json file.
    """
    validate_aws_config() 
    client = get_sqs_client()

    # Process the template and replace placeholders
    dynamic_values_dict = parse_dynamic_values(dynamic_values)
    messages = process_template(template_file, dynamic_values_dict)

    for message in messages:
        response = client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message),
        )
        print(f"Message sent. ID: {response['MessageId']}")


@sqs_app.command("generate-template")
def generate_template(file_path: str = "template.json"):
    """
    Generate a sample JSON file with placeholders.
    """
    validate_aws_config() 
    sample_messages = {
        "messages": [
            {
                "field1": "{{dynamic_value_1}}",
                "field2": "{{dynamic_value_2}}",
                "uuid": "{{uuid}}",
                "timestamp": "{{timestamp}}",
            }
        ]
    }

    with open(file_path, "w") as file:
        json.dump(sample_messages, file, indent=4)

    print(f"Sample template saved to {file_path}.")


def process_template(file_path: str, dynamic_values: dict):
    """
    Process the template file and replace placeholders with dynamic values.
    """

    validate_aws_config() 
    with open(file_path, "r") as file:
        template = json.load(file)

    messages = template.get("messages", [])


    processed_messages = []
    for message in messages:
        processed_message = {}
        for key, value in message.items():
            if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
                placeholder = value.strip("{}")
                if placeholder in dynamic_values:
                    processed_message[key] = dynamic_values[placeholder]
                elif placeholder == "uuid":
                    processed_message[key] = str(uuid.uuid4())
                elif placeholder == "timestamp":
                    processed_message[key] = datetime.now().isoformat()
                else:
                    raise ValueError(f"Unknown placeholder: {placeholder}")
            else:
                processed_message[key] = value
        processed_messages.append(processed_message)

    return processed_messages


def parse_dynamic_values(dynamic_values: str):
    """
    Parse dynamic key-value pairs provided via CLI.
    """

    validate_aws_config() 
    if not dynamic_values:
        return {}

    dynamic_dict = {}
    try:
        pairs = dynamic_values.split(",")
        for pair in pairs:
            key, value = pair.split("=")
            dynamic_dict[key.strip()] = value.strip()
    except Exception as e:
        raise ValueError(f"Error parsing dynamic values: {e}")
    return dynamic_dict
