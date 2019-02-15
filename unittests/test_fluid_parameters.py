#!/usr/bin/env python3
import pytest

from calculations.fluid_parameters import fluid_params


@pytest.mark.parametrize(
    'fluid, temperature, expected_params',
    (
        # exacly table parameters
        (
            'water',
            10,
            {'temperature': 10, 'density': 999.7, 'specific_heat': 4191, 'kinematic_viscosity': 0.000001306},
        ),
        (
            'water',
            350,
            {'temperature': 350, 'density': 574.4, 'specific_heat': 9504, 'kinematic_viscosity': 0.000000126},
        ),
        # interpolated parameters
        (
            'water',
            15,
            {'temperature': 15, 'density': 998.95, 'specific_heat': 4187, 'kinematic_viscosity': 0.000001156},
        ),
        (
            'water',
            51,
            {'temperature': 51, 'density': 987.61, 'specific_heat': 4174.5, 'kinematic_viscosity': 0.0000005482},
        ),
    ),
)
def test_fluid_params(fluid, temperature, expected_params):
    assert fluid_params(fluid, temperature) == expected_params
