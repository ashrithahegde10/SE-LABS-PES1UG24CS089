import pytest
from coupon_validator import coupon_discount, best_discount, is_expired


# -------------------------
# coupon_discount() tests
# -------------------------

def test_empty_cart_raises_error():
    with pytest.raises(ValueError, match="empty cart"):
        coupon_discount("WELCOME10", 0, True, "mon")


def test_welcome_coupon_for_new_user():
    assert coupon_discount("WELCOME10", 200, True, "mon") == 20


def test_welcome_coupon_for_existing_user():
    assert coupon_discount("WELCOME10", 200, False, "mon") == 0


def test_weekend_coupon_large_cart():
    assert coupon_discount("WEEKEND20", 600, False, "sat") == 120


def test_weekend_coupon_small_cart():
    assert coupon_discount("WEEKEND20", 300, False, "sun") == 50


def test_weekend_coupon_on_weekday():
    assert coupon_discount("WEEKEND20", 600, False, "mon") == 0


def test_flat100_coupon_eligible_cart():
    assert coupon_discount("FLAT100", 400, False, "mon") == 100


def test_flat100_coupon_ineligible_cart():
    assert coupon_discount("FLAT100", 300, False, "mon") == 0


def test_unknown_coupon():
    assert coupon_discount("INVALID", 400, True, "sat") == 0


# -------------------------
# best_discount() tests
# -------------------------

def test_best_discount_with_empty_coupon_list():
    assert best_discount([], 500, True, "sat") == 0


def test_best_discount_selects_highest_coupon():
    codes = ["WELCOME10", "WEEKEND20", "FLAT100"]
    assert best_discount(codes, 600, True, "sat") == 120


def test_best_discount_returns_zero_when_no_coupon_applies():
    assert best_discount(["WELCOME10", "WEEKEND20"], 200, False, "mon") == 0


# -------------------------
# is_expired() tests
# -------------------------

def test_zero_validity_is_expired():
    assert is_expired(10, 5, 0) is True


def test_negative_validity_is_expired():
    assert is_expired(10, 5, -1) is True


def test_coupon_expired_after_validity_period():
    assert is_expired(16, 5, 10) is True


def test_coupon_not_expired_within_validity_period():
    assert is_expired(15, 5, 10) is False


def test_coupon_not_expired_on_start_day():
    assert is_expired(5, 5, 10) is False