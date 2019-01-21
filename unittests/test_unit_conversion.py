#!/usr/bin.env python3
import pytest

from unit_convertion import unit_convertion


@pytest.mark.parametrize(
    'value, unit_from, unit_to, data_type, expected_value',
    (
        (1, 'm', 'm', 'lenght.csv', 1),
        (1, 'dm', 'm', 'lenght.csv', 0.1),
        (1, 'cm', 'm', 'lenght.csv', 0.01),
        (1, 'mm', 'm', 'lenght.csv', 0.001),
        (12, 'mm', 'cm', 'lenght.csv', 1.2),
        (1.2, 'cm', 'dm', 'lenght.csv', 0.12),
        (0.12, 'dm', 'm', 'lenght.csv', 0.012),
        (1, 'in', 'cm', 'lenght.csv', 2.54),
        (1, 'atm', 'bar', 'pressure.csv', 1.01325),
    ),
)
def test_unit_convertion(value, unit_from, unit_to, data_type, expected_value):
    assert unit_convertion(value, unit_from, unit_to, data_type) == expected_value


@pytest.mark.parametrize(
    'value, unit_from, unit_to, data_type, expected_message',
    (
        (11, 'mmm', 'm', 'lenght.csv', 'Not found mmm.'),
        (0.7, 'm', 'ddd', 'lenght.csv', 'Not found ddd.'),
        (0.7, 'sss', 'ddd', 'lenght.csv', 'Not found sss and ddd.'),
    ),
)
def test_unit_convertion_failed(value, unit_from, unit_to, data_type, expected_message):
    assert unit_convertion(value, unit_from, unit_to, data_type) == expected_message
