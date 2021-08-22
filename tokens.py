import json
import secrets
import time

import requests


def is_token_expired(token_dict: dict) -> bool:
    current_time = int(time.time())
    expiration_time = int(token_dict["expiration_time"])
    return expiration_time <= current_time


def get_new_token(old_token_dict: dict) -> dict:
    old_token_dict.pop("token")
    old_token_dict.pop("expiration_time")
    query_params = {
        "client_id": old_token_dict["client_id"],
        "client_secret": old_token_dict["client_secret"],
        "grant_type": "client_credentials"
    }

    response = requests.post("https://id.twitch.tv/oauth2/token", params=query_params)
    token_dict = format_token_dict({**response.json(), **old_token_dict})
    secrets.update_secret("twitch_oauth", json.dumps(token_dict))
    return token_dict


# We need to set the absolute epoch expiration time
def format_token_dict(token_dict: dict) -> dict:
    # Set expiration to be an hour earlier
    current_time = int(time.time()) - (60 * 60)
    expiration_time = token_dict["expires_in"] + current_time
    return {
        "client_id": token_dict["client_id"],
        "client_secret": token_dict["client_secret"],
        "token": token_dict["access_token"],
        "expiration_time": str(expiration_time)
    }


def get_valid_token() -> str:
    token_dict = json.loads(secrets.get_secret("twitch_oauth"))

    if is_token_expired(token_dict):
        token_dict = get_new_token()
    return token_dict["token"]
