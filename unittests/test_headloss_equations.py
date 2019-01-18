#!/usr/bin/env python3
import math

import pytest

from headloss_equations import darcy_weisbach_equation
from headloss_equations import hagen_poiseuille_equation
from headloss_equations import reynolds_equation


@pytest.mark.parametrize(
    'dfc, llc, length, diameter, density, velocity, expected_headloss',
    (
        (0.03, 0, 10, 0.1, 1000, 1, 1500),
        (0.03, 25, 20, 0.1, 998.2, 2, 61888.4),
        (0.015, 13.5, 97, 0.05, 971.83, 1.5, 46574.95),
    ),
)
def test_darcy_weisbach_equation(dfc, llc, length, diameter, density, velocity, expected_headloss):
    assert darcy_weisbach_equation(dfc, llc, length, diameter, density, velocity) == expected_headloss


@pytest.mark.parametrize('reynold, expected_dfc', ((1, 64), (64, 1), (2099, 0.03)))
def test_hagen_poiseuille_equation(reynold, expected_dfc):
    assert hagen_poiseuille_equation(reynold) == expected_dfc


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
