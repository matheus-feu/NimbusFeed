import logging


def ready_logger(stream, level) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    handler = logging.StreamHandler(stream)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


app_logger = ready_logger(None, logging.INFO)
