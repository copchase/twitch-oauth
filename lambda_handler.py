import tokens


def lambda_handler(event: dict, context) -> str:
    return tokens.get_valid_token()
