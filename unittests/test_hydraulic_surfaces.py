#!/usr/bin/env python3
import pytest

from hydraulic_surfaces import circular_pipe
from hydraulic_surfaces import get_internal_diameter
from hydraulic_surfaces import rectangular_dict


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


@pytest.mark.parametrize(
    'width, height, unit, expected_area', ((100, 200, 'mm', 0.02), (10, 20, 'cm', 0.02), (0.1, 0.2, 'm', 0.02))
)
def test_rectangular_dict(width, height, unit, expected_area):
    assert rectangular_dict(width, height, unit) == expected_area
