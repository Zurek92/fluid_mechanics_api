#!/usr/bin.env python3
import pytest

from unit_convertion import unit_convertion


@pytest.mark.parametrize(
    'value, unit_from, unit_to, data_type, expected_value',
    (
        (1, 'm', 'm', 'lenght', 1),
        (1, 'dm', 'm', 'lenght', 0.1),
        (1, 'cm', 'm', 'lenght', 0.01),
        (1, 'mm', 'm', 'lenght', 0.001),
        (12, 'mm', 'cm', 'lenght', 1.2),
        (1.2, 'cm', 'dm', 'lenght', 0.12),
        (0.12, 'dm', 'm', 'lenght', 0.012),
        (1, 'in', 'cm', 'lenght', 2.54),
        (1, 'atm', 'bar', 'pressure', 1.01325),
        (1, 'gal', 'l', 'volume', 3.785411784),
        (1, 'm3', 'dm3', 'volume', 1000),
        (1, 'gal', 'mm3', 'volume', 3785411.784),
        (1, 'h', 's', 'time', 3600),
        (1, 'm', 's', 'time', 60),
    ),
)
def test_unit_convertion(value, unit_from, unit_to, data_type, expected_value):
    assert unit_convertion(value, unit_from, unit_to, data_type) == expected_value


@pytest.mark.parametrize(
    'value, unit_from, unit_to, data_type, expected_message',
    (
        (11, 'mmm', 'm', 'lenght', 'Not found mmm.'),
        (0.7, 'm', 'ddd', 'lenght', 'Not found ddd.'),
        (0.7, 'sss', 'ddd', 'lenght', 'Not found sss and ddd.'),
    ),
)
def test_unit_convertion_failed(value, unit_from, unit_to, data_type, expected_message):
    assert unit_convertion(value, unit_from, unit_to, data_type) == expected_message
