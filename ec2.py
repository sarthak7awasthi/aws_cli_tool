import boto3
import typer
from config import validate_aws_config


ec2_app = typer.Typer(help="Commands to manage EC2 instances.")


def get_ec2_client():
    return boto3.client("ec2")

@ec2_app.command("list")
def list_instances():
    """
    List all EC2 instances with their IDs, state, and name.
    """
    validate_aws_config
    client = get_ec2_client()
    response = client.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            state = instance["State"]["Name"]
            name = next(
                (tag["Value"] for tag in instance.get("Tags", []) if tag["Key"] == "Name"),
                "N/A"
            )
            print(f"ID: {instance_id}, State: {state}, Name: {name}")

@ec2_app.command("start")
def start_instance(instance_id: str):
    """
    Start an EC2 instance by its ID.
    """
    validate_aws_config
    client = get_ec2_client()
    response = client.start_instances(InstanceIds=[instance_id])
    print(f"Starting instance {instance_id}. Current state: {response['StartingInstances'][0]['CurrentState']['Name']}")

@ec2_app.command("stop")
def stop_instance(instance_id: str):
    """
    Stop an EC2 instance by its ID.
    """
    validate_aws_config
    client = get_ec2_client()
    response = client.stop_instances(InstanceIds=[instance_id])
    print(f"Stopping instance {instance_id}. Current state: {response['StoppingInstances'][0]['CurrentState']['Name']}")

@ec2_app.command("terminate")
def terminate_instance(instance_id: str):
    """
    Terminate an EC2 instance by its ID.
    """
    validate_aws_config
    client = get_ec2_client()
    response = client.terminate_instances(InstanceIds=[instance_id])
    print(f"Terminating instance {instance_id}. Current state: {response['TerminatingInstances'][0]['CurrentState']['Name']}")
