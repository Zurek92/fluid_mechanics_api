#!/usr/bin/env python3
import math


def colebrook_equation(reynold, rel_roughness):
    """Returns darcy friction coefficient (dfc) for turbulent flow.

    :param reynold: reynold number [-]
    :param rel_roughness: relative roughness [-]
    """

    def left_side(dfc):
        return 1 / math.sqrt(dfc)

    def right_side(dfc, reynold, rel_roughness):
        return -2 * math.log10((2.51 / (reynold * math.sqrt(dfc)) + (rel_roughness / 3.71)))

    dfc = 20
    prev_dfc = 0
    while True:
        left_side_value = left_side(dfc)
        right_side_value = right_side(dfc, reynold, rel_roughness)
        diff = abs(dfc - prev_dfc) / 2
        prev_dfc = dfc
        if left_side_value - right_side_value < -0.001:
            dfc -= diff
        elif left_side_value - right_side_value > 0.001:
            dfc += diff
        else:
            return round(dfc, 3)


def darcy_friction_coefficient(reynolds, internal_dimension, roughness):
    """Returns dfc depends on flow laminar or turbulent.

    :param reynolds: reynolds number
    :param internal_dimension: internal dimension of pipe
    :param roughness: roughness of pipe
    """
    if reynolds > 2100:
        rel_roughness = relative_roughness(roughness, internal_dimension)
        return colebrook_equation(reynolds, rel_roughness)
    return hagen_poiseuille_equation(reynolds)


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
    return round((llc + dfc * length / diameter) * density * math.pow(velocity, 2) / 2, 0)


def hagen_poiseuille_equation(reynold):
    """Returns darcy friction coefficient for laminar flow.

    :param reynold: reynold number [-]
    """
    return round(64 / reynold, 3)


def relative_roughness(roughness, diameter):
    """Returns relative roughness.

    :param roughness: roughness of pipe [mm] or [m] (but the same as diameter)
    :param diameter: diameter of duct or pipe [mm] or [m]
    """
    return round(roughness / diameter, 8)


def reynolds_equation(velocity, diameter, viscosity):
    """Reynolds number equation.

    :param velocity: average velocity of fluid [m/s]
    :param diameter: hydraulic diameter of duct or pipe [m]
    :param viscosity: kinematic viscosity [s/m2]
    """
    return round(velocity * diameter / viscosity, 0)
