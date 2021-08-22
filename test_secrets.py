import secrets
from unittest.mock import MagicMock

from botocore.exceptions import ClientError


def test_get_secret_exception(mocker):
    mock_error = ClientError({"Error": {"Code": "ErrorCode"}}, "test_get_secret_exception")
    mock_secrets_client = MagicMock()
    mock_secrets_client.configure_mock(**{"get_secret_value.side_effect": mock_error})
    mocker.patch("boto3.client", return_value=mock_secrets_client)

    result = secrets.get_secret("my-secret")

    assert result is None


def test_get_secret(mocker):
    mock_secret = {"SecretString": "hello world"}
    mock_secrets_client = MagicMock()
    mock_secrets_client.configure_mock(**{"get_secret_value.return_value": mock_secret})
    mocker.patch("boto3.client", return_value=mock_secrets_client)

    result = secrets.get_secret("my-secret")

    assert result == "hello world"


def test_update_secret_exception(mocker):
    mock_error = ClientError({"Error": {"Code": "ErrorCode"}}, "test_update_secret_exception")
    mock_secrets_client = MagicMock()
    mock_secrets_client.configure_mock(**{"update_secret.side_effect": mock_error})
    mocker.patch("boto3.client", return_value=mock_secrets_client)

    result = secrets.update_secret("my-secret", "new-secret")

    assert result is False


def test_update_secret(mocker):
    mock_secrets_client = MagicMock()
    mock_secrets_client.configure_mock(**{"update_secret.return_value": None})
    mocker.patch("boto3.client", return_value=mock_secrets_client)

    result = secrets.update_secret("my-secret", "new-secret")

    assert result is True
