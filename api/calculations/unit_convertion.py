#!/usr/bin/env python3
"""Convert units.

Configuration files are in ./csv_data/unit_convertion/<data_type>.csv
Available types: lenght.csv, pressure.csv, volume.csv, time.csv
"""
import csv
import os

script_dir = os.path.dirname(__file__)
rel_path = "../csv_data/unit_convertion/"


def unit_convertion(value, unit_from, unit_to, data_type):
    """Unit converion.

    :param value: input value to convert
    :param unit_from: input unit
    :param unit_to: output unit with new value
    :param data_type: values are taken from csv_data/unit_convertion/<data_type>.csv
    """
    with open(os.path.join(script_dir, rel_path, f'{data_type}.csv'), 'r') as csv_file:
        csv_lenghts = csv.DictReader(csv_file)
        required_matches = 0
        for row in csv_lenghts:
            if row['unit'] == unit_from:
                converter_from = float(row['converter'])
                required_matches += 1
            if row['unit'] == unit_to:
                converter_to = float(row['converter'])
                required_matches += 2
            if required_matches == 3:
                return value * converter_from / converter_to
        return unit_not_found_message(required_matches, unit_from, unit_to)


def unit_not_found_message(required_matches, unit_from, unit_to):
    NOT_FOUND_MESSAGES = [f'Not found {unit_from} and {unit_to}.', f'Not found {unit_to}.', f'Not found {unit_from}.']
    return NOT_FOUND_MESSAGES[required_matches]
