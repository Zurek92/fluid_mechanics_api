#!/usr/bin/env python3
import pytest

from headloss_equations import darcy_weisbach_equation


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
