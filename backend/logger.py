import logging

logger = logging.getLogger("mylogger")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:\t%(message)s")

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger.addHandler(handler)
