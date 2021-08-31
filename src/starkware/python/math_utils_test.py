import pytest

from starkware.python.math_utils import (
    div_ceil, div_mod, ec_add, ec_double, ec_mult, is_power_of_2, is_quad_residue, next_power_of_2,
    safe_div, safe_log2, sqrt)


def test_ec_add():
    # Checked using sage.
    # E = EllipticCurve(GF(331),[0,0,0,-1,1])
    # print E(279, 293) + E(66, 192)
    assert ec_add((279, 293), (66, 192), 331) == (224, 33)
    with pytest.raises(AssertionError):
        # x coordinates are equal - should throw an AssertionError.
        ec_add((279, 293), (279, 38), 331)


def test_ec_double():
    # Checked using sage.
    # E = EllipticCurve(GF(3331),[0,0,0,-1,1])
    # print 2 * E(2817, 1099)
    assert ec_double((2817, 1099), -1, 3331) == (1166, 3163)
    with pytest.raises(AssertionError):
        # Should throw an AssertionError since y == 0.
        ec_double((1, 0), -1, 3331)


def test_ec_mult():
    # Checked using sage.
    # E = EllipticCurve(GF(33331),[0,0,0,2,1])
    # print 123 * E(25078, 18096)
    assert ec_mult(123, (25078, 18096), 2, 33331) == (12009, 15845)


def test_safe_div():
    for x in [2, 3, 5, 6, 10, 12, -2, -3, -10]:
        assert safe_div(60, x) * x == 60
    for val in [0, 7, 120]:
        with pytest.raises(AssertionError):
            safe_div(60, val)


def test_div_ceil():
    assert div_ceil(7, 3) == 3
    assert div_ceil(8, 2) == 4
    assert div_ceil(9, 2) == 5


def test_safe_log2():
    for i in range(0, 64):
        assert safe_log2(2 ** i) == i
    for val in [-1, 0, 3]:
        with pytest.raises(AssertionError):
            safe_log2(val)


def test_next_power_of_2():
    assert next_power_of_2(1) == 1
    assert next_power_of_2(2) == 2
    assert next_power_of_2(3) == 4
    assert next_power_of_2(4) == 4
    assert next_power_of_2(5) == 8
    assert next_power_of_2(2 ** 128) == 2 ** 128
    assert next_power_of_2(2 ** 128 + 1) == 2 ** 129
    assert next_power_of_2(2 ** 129 - 1) == 2 ** 129
    assert next_power_of_2(2 ** 129) == 2 ** 129
    with pytest.raises(AssertionError):
        next_power_of_2(-2)


def test_div_mod():
    assert div_mod(2, 3, 5) == 4
    with pytest.raises(AssertionError):
        div_mod(8, 10, 5)


def test_is_quad_residue():
    assert is_quad_residue(2, 7)
    assert not is_quad_residue(3, 7)


def test_sqrt():
    assert sqrt(2, 7) == 3


def test_is_power_of_2():
    assert not is_power_of_2(0)
    assert is_power_of_2(1)
    assert is_power_of_2(8)
    assert not is_power_of_2(3)
    assert is_power_of_2(2 ** 129)
    assert not is_power_of_2(2 ** 129 + 1)
