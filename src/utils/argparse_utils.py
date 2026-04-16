import argparse
from datetime import datetime


def argparse_hhmm_time(value: str):
    try:
        return datetime.strptime(value, "%H:%M").time()
    except ValueError:
        raise argparse.ArgumentTypeError("Time must be in HH:MM format")