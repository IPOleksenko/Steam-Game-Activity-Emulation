import logging

from application import app
from utils import DLL


def main():
    DLL.initialize()
    app()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
