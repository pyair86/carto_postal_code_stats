import logging


class Logger:

    logging.basicConfig(filename="carto_log.log", format="%(asctime)s %(message)s")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
