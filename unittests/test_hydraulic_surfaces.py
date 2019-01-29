#!/usr/bin/env python3
import math

import pytest

from hydraulic_surfaces import angle_in_partial_filled_pipe
from hydraulic_surfaces import circular_pipe
from hydraulic_surfaces import circular_water_cross_sectional_area
from hydraulic_surfaces import circular_wetted_perimeter
from hydraulic_surfaces import get_internal_diameter
from hydraulic_surfaces import hydraulic_radius
from hydraulic_surfaces import rectangular_dict


@pytest.mark.parametrize(
    'diameter, height, expected_angle',
    ((1, 1, math.pi), (1, 0.5, math.pi / 2), (1, 0, 0), (1, 0.14644, math.pi / 4), (1, 0.85356, 3 * math.pi / 4)),
)
def test_angle_in_partial_filled_pipe(diameter, height, expected_angle):
    assert round(angle_in_partial_filled_pipe(diameter, height), 4) == round(expected_angle, 4)


@pytest.mark.parametrize(
    'angle, diameter, height, expected_area', ((0, 1, 0, 0), (1.5707, 1, 0.5, 0.392675), (3.1416, 1, 1, 0.785398))
)
def test_circular_water_cross_sectional_area(angle, diameter, height, expected_area):
    assert round(circular_water_cross_sectional_area(angle, diameter, height), 6) == expected_area


@pytest.mark.parametrize('angle, diameter, expected_perimeter', ((math.pi, 3, 3 * math.pi), (2, 1, 2), (0, 3, 0)))
def test_circular_wetted_perimeter(angle, diameter, expected_perimeter):
    assert circular_wetted_perimeter(angle, diameter) == expected_perimeter


@pytest.mark.parametrize(
    'diameter, unit, expected_area', ((100, 'mm', 0.007854), (10, 'cm', 0.007854), (0.1, 'm', 0.007854))
)
def test_circular_pipe(diameter, unit, expected_area):
    assert round(circular_pipe(diameter, unit), 6) == expected_area


@pytest.mark.parametrize(
    'nominal, material, expected_diameter', ((25, 'steel', 27.2), (150, 'steel', 155.4), (155, 'steel', None))
)
def test_get_internal_diameter(nominal, material, expected_diameter):
    assert get_internal_diameter(nominal, material) == expected_diameter


@pytest.mark.parametrize('area, perimeter, expected_radius', ((2, 1, 2), (3, 2, 1.5)))
def test_hydraulic_radius(area, perimeter, expected_radius):
    assert hydraulic_radius(area, perimeter) == expected_radius


@pytest.mark.parametrize(
    'width, height, unit, expected_area', ((100, 200, 'mm', 0.02), (10, 20, 'cm', 0.02), (0.1, 0.2, 'm', 0.02))
)
def test_rectangular_dict(width, height, unit, expected_area):
    assert rectangular_dict(width, height, unit) == expected_area
