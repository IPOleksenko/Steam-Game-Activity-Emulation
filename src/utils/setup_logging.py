import logging


def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(process)d] %(levelname)s: %(message)s")
