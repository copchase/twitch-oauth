from logzero import logger

import tokens


def lambda_handler(event: dict, context) -> str:
    if "warmup" in event:
        return

    try:
        return tokens.get_valid_token()
    except Exception as e:
        logger.exception(e)
        return None
