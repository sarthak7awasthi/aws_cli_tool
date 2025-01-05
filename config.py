import os
from dotenv import load_dotenv

load_dotenv()  

def validate_aws_config():
    """
    Validate AWS configuration and raise an error if any required variable is missing.
    """
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_DEFAULT_REGION")

    if not access_key:
        raise Exception("AWS_ACCESS_KEY_ID is missing. Check your .env file.")
    if not secret_key:
        raise Exception("AWS_SECRET_ACCESS_KEY is missing. Check your .env file.")
    if not region:
        raise Exception("AWS_DEFAULT_REGION is missing. Check your .env file.")
