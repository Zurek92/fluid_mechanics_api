#!/usr/bin/env python3
import math

import pytest


from headloss_equations import colebrook_equation
from headloss_equations import darcy_friction_coefficient
from headloss_equations import darcy_weisbach_equation
from headloss_equations import hagen_poiseuille_equation
from headloss_equations import relative_roughness
from headloss_equations import reynolds_equation


@pytest.mark.parametrize(
    'reynold, rel_roughness, expected_dfc',
    (
        (10000, 0.04, 0.067),
        (10000, 0.005, 0.038),
        (100000, 0.001, 0.022),
        (10000000, 0.01, 0.038),
        (10000000, 0.00001, 0.009),
    ),
)
def test_colebrook_equation(reynold, rel_roughness, expected_dfc):
    assert colebrook_equation(reynold, rel_roughness) == expected_dfc


@pytest.mark.parametrize(
    'reynolds, internal_dimension, roughness, expected_dfc', ((2000, 100, 1.5, 0.032), (20000, 100, 1.5, 0.046))
)
def test_darcy_friction_coefficient(reynolds, internal_dimension, roughness, expected_dfc):
    assert darcy_friction_coefficient(reynolds, internal_dimension, roughness) == expected_dfc


@pytest.mark.parametrize(
    'dfc, llc, length, diameter, density, velocity, expected_headloss',
    (
        (0.03, 0, 10, 0.1, 1000, 1, 1500),
        (0.03, 25, 20, 0.1, 998.2, 2, 61888),
        (0.015, 13.5, 97, 0.05, 971.83, 1.5, 46575),
    ),
)
def test_darcy_weisbach_equation(dfc, llc, length, diameter, density, velocity, expected_headloss):
    assert darcy_weisbach_equation(dfc, llc, length, diameter, density, velocity) == expected_headloss


@pytest.mark.parametrize('reynold, expected_dfc', ((1, 64), (64, 1), (2099, 0.03)))
def test_hagen_poiseuille_equation(reynold, expected_dfc):
    assert hagen_poiseuille_equation(reynold) == expected_dfc


@pytest.mark.parametrize(
    'roughness, diameter, expected_output',
    (
        # in mm values
        (0.01, 100, 0.0001),
        (0.015, 50, 0.0003),
        (1, 100, 0.01),
        # in m values
        (0.001, 0.1, 0.01),
        (0.005, 0.2, 0.025),
    ),
)
def test_relative_roughness(roughness, diameter, expected_output):
    assert relative_roughness(roughness, diameter) == expected_output


@pytest.mark.parametrize(
    'velocity, diameter, viscosity, expected_reynolds',
    (
        (2, 0.1, 1.3065 * math.pow(10, -6), 153081),
        (3, 0.05, 1.0035 * math.pow(10, -6), 149477),
        (0.5, 0.02, 0.3643 * math.pow(10, -6), 27450),
    ),
)
def test_reynolds_equation(velocity, diameter, viscosity, expected_reynolds):
    assert reynolds_equation(velocity, diameter, viscosity) == expected_reynolds
