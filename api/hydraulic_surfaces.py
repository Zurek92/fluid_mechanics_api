#!/usr/bin/env python3
"""Areas of pipe, ducts or hydraulic diameters."""
import math

from unit_convertion import unit_convertion


def circular_pipe(diameter, unit):
    """Circular area in [m2].
    :param diameter: value of internal diameter
    :param unit: unit of diameter e.g.: [mm] or [m]
    """
    converted_diameter = unit_convertion(diameter, unit, 'm', 'lenght.csv')
    return round(math.pow(converted_diameter, 2) * math.pi / 4, 10)


def rectangular_dict(width, height, unit):
    """Rectangular area in [m2].

    :param width: duct width (A - dimension)
    :param height: duct height (B - dimension)
    :param unit: unit od dimensions e.g.: [mm] or [m]
    """
    conversion_value = math.pow(unit_convertion(1, unit, 'm', 'lenght.csv'), 2)
    return round(width * height * conversion_value, 10)
