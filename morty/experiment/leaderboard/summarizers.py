import csv
from collections import Iterable


def summarize_training(csv_file: Iterable[str]):
    """ """
    reader = csv.DictReader(csv_file)
