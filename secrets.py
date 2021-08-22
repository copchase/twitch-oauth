import boto3
from botocore.exceptions import ClientError
from logzero import logger
from typing import Union


def get_secret(secret_name: str) -> Union[str, bytes]:
    try:
        # client is init here for easier mocking during testing
        client = boto3.client("secretsmanager")
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            logger.error(f"The requested secret {secret_name} was not found")
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            logger.error(f"The request was invalid due to: {str(e)}")
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            logger.error(f"The request had invalid params: {str(e)}")
        elif e.response["Error"]["Code"] == "DecryptionFailure":
            logger.error(f"The requested secret can't be decrypted using the provided KMS key: {str(e)}")
        elif e.response["Error"]["Code"] == "InternalServiceError":
            logger.error(f"An error occurred on service side: {str(e)}")
        return None
    else:
        # Secrets Manager decrypts the secret value using the associated KMS CMK
        # Depending on whether the secret was a string or binary, only one of these fields will be populated
        if "SecretString" in get_secret_value_response:
            text_secret_data = get_secret_value_response["SecretString"]
        else:
            binary_secret_data = get_secret_value_response["SecretBinary"]

        secret_data = text_secret_data or binary_secret_data
        return secret_data


# the boolean returns to show if the operation was successful
def update_secret(secret_name: str, secret_string: str) -> bool:
    try:
        client = boto3.client("secretsmanager")
        client.update_secret(
            SecretId=secret_name,
            SecretString=secret_string
        )
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            logger.error(f"The requested secret {secret_name} was not found")
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            logger.error(f"The request was invalid due to: {str(e)}")
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            logger.error(f"The request had invalid params: {str(e)}")
        elif e.response["Error"]["Code"] == "EncryptionFailure":
            logger.error(f"The requested secret can't be encrypted using the provided KMS key: {str(e)}")
        elif e.response["Error"]["Code"] == "InternalServiceError":
            logger.error(f"An error occurred on service side: {str(e)}")
        elif e.response["Error"]["Code"] == "LimitExceededException":
            logger.error(f"The request is being rate limited: {str(e)}")
        elif e.response["Error"]["Code"] == "ResourceExistsException":
            logger.error(f"The request is attempting to update a versioned secret: {str(e)}")
        elif e.response["Error"]["Code"] == "MalformedPolicyDocumentException":
            logger.error(f"Resource policy is malformed for this request: {str(e)}")
        elif e.response["Error"]["Code"] == "PreconditionNotMetException":
            logger.error(f"Permission precondition was not met: {str(e)}")

    return False
