import secrets
import time

import boto3
import requests


def lambda_handler(event: dict, context) -> dict:
    token_dict = secrets.get_secret("twitch_oauth")

    if is_token_expired(token_dict):
        return None
    return {}


def is_token_expired(token_dict: dict) -> bool:
    current_time = int(time.time()) - 60
    expiration_date = token_dict["expiration"]
    return expiration_date <= current_time


def get_new_token() -> str:
    return ""
