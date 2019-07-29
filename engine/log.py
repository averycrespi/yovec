import logging


LOGGER_NAME = 'yovec'


def setup_logger(debug: bool=False):
    """Setup a custom logger."""
    formatter = logging.Formatter(fmt='%(asctime)s - %(module)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger('yovec')
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    logger.addHandler(handler)
