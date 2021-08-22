import json
import secrets
import time

import boto3
import requests

import tokens


def lambda_handler(event: dict, context) -> str:
    return tokens.get_valid_token()
