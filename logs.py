import boto3
import typer
from config import validate_aws_config

logs_app = typer.Typer(help="Commands to manage CloudWatch logs.")


def get_logs_client():
    return boto3.client("logs")


@logs_app.command("list-groups")
def list_log_groups():
    """
    List all CloudWatch log groups.
    """
    validate_aws_config
    client = get_logs_client()
    paginator = client.get_paginator("describe_log_groups")
    for page in paginator.paginate():
        log_groups = page.get("logGroups", [])
        for group in log_groups:
            print(f"Log Group Name: {group['logGroupName']}")
            print(f"Stored Bytes: {group.get('storedBytes', 0)}")
            print("-" * 30)


@logs_app.command("list-streams")
def list_log_streams(log_group_name: str):
    """
    List all log streams in a specific log group.
    """
    validate_aws_config
    client = get_logs_client()
    paginator = client.get_paginator("describe_log_streams")
    for page in paginator.paginate(logGroupName=log_group_name):
        log_streams = page.get("logStreams", [])
        for stream in log_streams:
            print(f"Log Stream Name: {stream['logStreamName']}")
            print(f"Creation Time: {stream.get('creationTime')}")
            print("-" * 30)


@logs_app.command("get-events")
def get_log_events(log_group_name: str, log_stream_name: str, start_time: int = None, end_time: int = None):
    """
    Retrieve log events from a specific log stream.
    """
    validate_aws_config
    client = get_logs_client()
    params = {
        "logGroupName": log_group_name,
        "logStreamName": log_stream_name,
        "startFromHead": True,
    }
    if start_time:
        params["startTime"] = start_time
    if end_time:
        params["endTime"] = end_time

    response = client.get_log_events(**params)
    events = response.get("events", [])
    for event in events:
        print(f"Timestamp: {event['timestamp']}")
        print(f"Message: {event['message']}")
        print("-" * 30)
