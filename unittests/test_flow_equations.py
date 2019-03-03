#!/usr/bin/env python3
import pytest

from calculations.flow_equations import manning_equation, velocity_equation


@pytest.mark.parametrize(
    'hydraulic_radius, manning_coefficient, slope, expected_velocity',
    ((1, 0.013, 0.01, 7.69), (0.5, 0.013, 0.01, 4.85), (0.5, 0.013, 0.005, 3.43), (0.025, 0.013, 0.05, 1.47)),
)
def test_manning_equation(hydraulic_radius, manning_coefficient, slope, expected_velocity):
    assert round(manning_equation(hydraulic_radius, manning_coefficient, slope), 2) == expected_velocity


@pytest.mark.parametrize(
    'flow, flow_unit, area, expected_velocity',
    ((10, 'm3/h', 0.002777, 1), (0.01, 'm3/s', 0.1, 0.1), (-0.01, 'm3/s', 0.1, -0.1)),
)
def test_velocity_equation(flow, flow_unit, area, expected_velocity):
    assert velocity_equation(flow, flow_unit, area) == expected_velocity


@pytest.mark.parametrize('flow, flow_unit, area', ((10, 'm3/km', 12), (10, 'm3', 12), (5, 'm/s', 5)))
def test_velocity_equation_failed(flow, flow_unit, area):
    assert velocity_equation(flow, flow_unit, area) == 'Wrong volume flow rate!'
