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


def angle_in_partial_filled_pipe(diameter, height):
    """Returns half of angle in partial filled circle pipe (in radians).

    Required to calculate area of cross sectional area of water and wetted perimeter.
    :param diameter: diameter of pipe [mm] or [m] but the same as height
    :param height: height of water in pipe
    """
    return math.acos(1 - (2 * height / diameter))


def circular_water_cross_sectional_area(angle, diameter, height):
    """Returns circle wetted perimeter.

    :param angle: angle in radians from angle_in_partial_filled_pipe function
    :param diameter: diameter of pipe [m]
    :param height: height of water in pipe
    """
    return (angle * math.pow(diameter, 2) - (diameter - 2 * height) * (diameter * math.sin(angle))) / 4


def circular_wetted_perimeter(angle, diameter):
    """Returns circle wetted perimeter.

    :param angle: angle in radians from angle_in_partial_filled_pipe function
    :param diameter: diameter of pipe [m]
    """
    return angle * diameter


def rectangular_wetted_perimeter(width, height):
    """Returns rectangular wetted perimeter in open channel.

    :param width: width of rectangular channel
    :param height: height of water in open channel
    """
    return width + 2 * height


def hydraulic_radius(area, perimeter):
    """Hydraulic radius [m].

    :param area: cross sectional area [m2]
    :param perimeter: wetted perimeter [m]
    """
    return area / perimeter
