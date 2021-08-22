import time
from unittest.mock import MagicMock

import pytest

import tokens


def test_is_token_expired_valid_token():
    expiration_time = int(time.time()) + 10000
    valid_token_dict = {"expiration_time": str(expiration_time)}

    result = tokens.is_token_expired(valid_token_dict)

    assert result is False


def test_is_token_expired_stale_token():
    stale_token_dict = {"expiration_time": str(-1 * 2**63)}

    result = tokens.is_token_expired(stale_token_dict)

    assert result is True


def test_get_new_token(mocker):
    mock_logger = mocker.patch("tokens.logger.error")
    mocker.patch("requests.post")
    mocker.patch("tokens.format_token_dict", return_value={"hello": "world"})
    mocker.patch("secrets.update_secret", return_value=True)
    old_token_dict = {
        "client_id": "client_id",
        "client_secret": "client_secret"
    }

    result = tokens.get_new_token(old_token_dict)

    assert result["hello"] == "world"
    mock_logger.assert_not_called()


def test_get_new_token_secret_update_error(mocker):
    mock_logger = mocker.patch("tokens.logger.error")
    mocker.patch("requests.post")
    mocker.patch("tokens.format_token_dict", return_value={"hello": "world"})
    mocker.patch("secrets.update_secret", return_value=False)
    old_token_dict = {
        "client_id": "client_id",
        "client_secret": "client_secret"
    }

    result = tokens.get_new_token(old_token_dict)

    assert result["hello"] == "world"
    mock_logger.assert_called_once()


def test_get_new_token_request_error(mocker):
    mock_response = MagicMock()
    mock_response.configure_mock(**{"raise_for_status.side_effect": Exception()})
    mocker.patch("requests.post", return_value=mock_response)
    old_token_dict = {
        "client_id": "client_id",
        "client_secret": "client_secret"
    }

    with pytest.raises(Exception):
        tokens.get_new_token(old_token_dict)


def test_format_token_dict():
    current_time = int(time.time())
    token_dict = {
        "client_id": "client_id",
        "client_secret": "client_secret",
        "access_token": "token",
        "expires_in": 250000  # about the same magnitude as the real response
    }

    result = tokens.format_token_dict(token_dict)

    assert int(result["expiration_time"]) > current_time


def test_format_token_dict_bad_dict(mocker):
    token_dict = {}

    with pytest.raises(KeyError):
        tokens.format_token_dict(token_dict)


def test_get_valid_token(mocker):
    mocker.patch("secrets.get_secret", return_value="""{"token": "my token"}""")
    mocker.patch("tokens.is_token_expired", return_value=False)
    mock_get_new_token = mocker.patch("tokens.get_new_token", return_value={"token": "my new token"})


    result = tokens.get_valid_token()

    assert result == "my token"
    mock_get_new_token.assert_not_called()


def test_get_valid_token_stale_token(mocker):
    mocker.patch("secrets.get_secret", return_value="{}")
    mocker.patch("tokens.is_token_expired", return_value=True)
    mock_get_new_token = mocker.patch("tokens.get_new_token", return_value={"token": "my new token"})

    result = tokens.get_valid_token()

    assert result == "my new token"
    mock_get_new_token.assert_called()
