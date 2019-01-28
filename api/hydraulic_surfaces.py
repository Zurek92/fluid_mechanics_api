#!/usr/bin/env python3
"""Areas of pipe, ducts or hydraulic diameters."""
import csv
import math
import os

from unit_convertion import unit_convertion

script_dir = os.path.dirname(__file__)
rel_path = "csv_data/pipes/"


def circular_pipe(diameter, unit):
    """Circular area in [m2].
    :param diameter: value of internal diameter
    :param unit: unit of diameter e.g.: [mm] or [m]
    """
    converted_diameter = unit_convertion(diameter, unit, 'm', 'lenght')
    return round(math.pow(converted_diameter, 2) * math.pi / 4, 10)


def get_internal_diameter(nominal, material):
    """Get internal dimension (diameter) of pipe.

    :param nominal: nominal diameter of pipe e.g.: for steel it's DN
    :param material: material of pipe in csv_data/pipes/
    """
    with open(os.path.join(script_dir, rel_path, f'{material}.csv')) as csv_file:
        data = csv.DictReader(csv_file)
        nominal = str(nominal)
        for row in data:
            if row['DN'] == nominal:
                return float(row['internal'])


def get_internal_diameters(material):
    """Get internal dimension (diameter) of all pipes.

    :param material: material of pipe in csv_data/pipes/
    """
    with open(os.path.join(script_dir, rel_path, f'{material}.csv')) as csv_file:
        data = csv.DictReader(csv_file)
        for row in data:
            yield int(row['DN']), float(row['internal'])


def rectangular_dict(width, height, unit):
    """Rectangular area in [m2].

    :param width: duct width (A - dimension)
    :param height: duct height (B - dimension)
    :param unit: unit od dimensions e.g.: [mm] or [m]
    """
    conversion_value = math.pow(unit_convertion(1, unit, 'm', 'lenght'), 2)
    return round(width * height * conversion_value, 10)
