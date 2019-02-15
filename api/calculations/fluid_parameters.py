#!/usr/bin/env python3
import csv
import os

script_dir = os.path.dirname(__file__)
rel_path = "../csv_data/fluids/"


def interpolate_data(diff, prev_value, current_value):
    """Returns interpolated value.

    :param diff: difference between values e.g:
    temperature from user: 71 (requested value),
    temperature previous: 70,
    temperature next: 80,
    diff = (temperature_from_user - temperature_previous) / (temperature_next - temperature_previous)
    :param prev_value: previous value
    :param current_value: next value
    """
    return prev_value + diff * (current_value - prev_value)


def dict_values_convert_to_float(dict_to_convert):
    """Simple converting dict values from string to float.

    :param dict_to_convert: dict from csv file with string values.
    """
    return {key: float(value) for key, value in dict_to_convert.items()}


def fluid_params(fluid, temperature):
    """Returns fluid parameters in requested temperature.

    :param fluid: requested fluid which exist in csv_data/fluids/
    :param temperature: requested temperature of fluid
    """
    with open(os.path.join(script_dir, rel_path, f'{fluid}.csv'), 'r') as csv_file:
        data = csv.DictReader(csv_file)
        prev_row = None
        for row in data:
            current_row_temp = int(row['temperature'])
            if current_row_temp == temperature:
                return dict_values_convert_to_float(row)
            elif prev_row and current_row_temp > temperature:
                prev_row = dict_values_convert_to_float(prev_row)
                current_row = dict_values_convert_to_float(row)
                diff = (temperature - prev_row['temperature']) / (current_row['temperature'] - prev_row['temperature'])
                return {
                    'temperature': temperature,
                    'density': interpolate_data(diff, prev_row['density'], current_row['density']),
                    'specific_heat': interpolate_data(diff, prev_row['specific_heat'], current_row['specific_heat']),
                    'kinematic_viscosity': interpolate_data(
                        diff, prev_row['kinematic_viscosity'], current_row['kinematic_viscosity']
                    ),
                }
            prev_row = row
