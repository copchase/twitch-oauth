from logzero import logger

import tokens


def lambda_handler(event: dict, context) -> str:
    try:
        return tokens.get_valid_token()
    except Exception as e:
        logger.exception(e)
        return None
