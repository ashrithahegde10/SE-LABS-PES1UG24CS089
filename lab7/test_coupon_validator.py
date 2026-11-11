
from hypothesis import given, strategies as st
from coupon_validator import split_code, most_expensive, expiry_days


# Fuzz testing: split_code
@given(st.text() | st.none())
def test_split_code_no_crash(s):
    split_code(s)


def test_split_code_valid():
    assert split_code("save-20") == ("SAVE", 20)


# Fuzz testing: most_expensive
@given(st.text() | st.none())
def test_most_expensive_no_crash(s):
    most_expensive(s)


def test_most_expensive_valid():
    assert most_expensive("199,49.5,320") == 320.0


# Fuzz testing: expiry_days
@given(st.text() | st.none())
def test_expiry_days_no_crash(s):
    expiry_days(s)


def test_expiry_days_valid():
    assert expiry_days("2025-01-01") == 366
