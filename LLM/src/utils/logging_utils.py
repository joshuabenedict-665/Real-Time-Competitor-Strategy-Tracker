from loguru import logger

def setup_logging(level: str = "INFO"):
    logger.remove()
    logger.add(lambda msg: print(msg, end=""), level=level.upper())
    return logger
