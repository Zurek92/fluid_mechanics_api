#!/usr/bin/env python3
from unit_convertion import unit_convertion


def velocity_equation(flow, flow_unit, area):
    """Calculate average velocity.

    :param flow: volume flow rate
    :param flow_unit: flow unit e.g.: [m3/h], [m3/s]
    :param area: area of pipe's cross section [m2]"""
    try:
        volume_unit, time_unit = flow_unit.split('/')
        volume_convertion = unit_convertion(1, volume_unit, 'm3', 'volume')
        time_convertion = unit_convertion(1, time_unit, 's', 'time')
        return round((flow * volume_convertion / time_convertion) / area, 2)
    except (ValueError, TypeError):
        return 'Wrong volume flow rate!'
