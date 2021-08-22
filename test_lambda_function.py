import lambda_function

def test_lambda_handler(mocker):
    mocker.patch("tokens.get_valid_token")

    lambda_function.lambda_handler({}, None)
