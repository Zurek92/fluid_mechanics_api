#!/usr/bin/env python3
import pytest

from flow_equations import velocity_equation


@pytest.mark.parametrize(
    'flow, flow_unit, area, expected_velocity',
    ((10, 'm3/h', 0.00278, 1), (0.01, 'm3/s', 0.1, 0.1), (-0.01, 'm3/s', 0.1, -0.1)),
)
def test_velocity_equation(flow, flow_unit, area, expected_velocity):
    assert velocity_equation(flow, flow_unit, area) == expected_velocity


@pytest.mark.parametrize('flow, flow_unit, area', ((10, 'm3/km', 12), (10, 'm3', 12), (5, 'm/s', 5)))
def test_velocity_equation_failed(flow, flow_unit, area):
    assert velocity_equation(flow, flow_unit, area) == 'Wrong volume flow rate!'
