#!/usr/bin/env python3
import math


def darcy_weisbach_equation(dfc, llc, length, diameter, density, velocity):
    """Headloss equation.

    Returns pressure loss in Pascals [Pa].
    :param dfc: darcy friction coefficient (or darcy friction factor) [-]
    :param llc: local loss coefficient [-]
    :param length: length of duct or pipe [m]
    :param diameter: hydraulic diameter of duct or pipe [m]
    :param density: density of fluid [kg/m3]
    :param velocity: average velocity of fluid [m/s]
    """
    return round((llc + dfc * length / diameter) * density * math.pow(velocity, 2) / 2, 2)
