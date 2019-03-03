#!/usr/bin/env python3
"""Convert units.

Configuration files are in ./csv_data/unit_convertion/<data_type>.csv
Available types: lenght.csv, pressure.csv, volume.csv, time.csv
"""
import csv
import math
import os

script_dir = os.path.dirname(__file__)
rel_path = "../csv_data/unit_convertion/"


def round_units(number, significant):
    """Round-off a number to a given number of significant digits.

    :param number: given number
    :param significant: significant digits
    """
    number_integer_part = math.floor(number)
    number_decimal_part = number - number_integer_part
    if number == 0:
        return 0
    int_precision = 0
    while number_integer_part >= 1:
        int_precision += 1
        number_integer_part /= 10
    digits = significant - int_precision
    if digits <= 0:
        # result is integer > 0
        return int(round(number * pow(10, digits)) / pow(10, digits))
    elif digits == significant:
        # float < 0
        float_precision = significant
        while number_decimal_part <= 0.1:
            float_precision += 1
            number_decimal_part *= 10
        return round(number, float_precision)
    # float > 0 but with decimal part
    return round(number, digits)


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
                return round_units(value * converter_from / converter_to, 5)
        return unit_not_found_message(required_matches, unit_from, unit_to)


def unit_not_found_message(required_matches, unit_from, unit_to):
    NOT_FOUND_MESSAGES = [f'Not found {unit_from} and {unit_to}.', f'Not found {unit_to}.', f'Not found {unit_from}.']
    return NOT_FOUND_MESSAGES[required_matches]
