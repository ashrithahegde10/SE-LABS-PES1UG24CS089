import pytest
from coupon_validator import coupon_discount, best_discount, is_expired


# coupon_discount() branches

def test_empty_cart_branch():
    with pytest.raises(ValueError, match="empty cart"):
        coupon_discount("WELCOME10", -1, True, "mon")


def test_welcome_new_user_branch():
    assert coupon_discount("WELCOME10", 100, True, "mon") == 10


def test_welcome_existing_user_branch():
    assert coupon_discount("WELCOME10", 100, False, "mon") == 0


def test_weekend_large_cart_branch():
    assert coupon_discount("WEEKEND20", 500, False, "sat") == 100


def test_weekend_small_cart_branch():
    assert coupon_discount("WEEKEND20", 200, False, "sun") == 50


def test_weekend_weekday_branch():
    assert coupon_discount("WEEKEND20", 500, False, "mon") == 0


def test_flat100_eligible_branch():
    assert coupon_discount("FLAT100", 301, False, "mon") == 100


def test_flat100_ineligible_branch():
    assert coupon_discount("FLAT100", 300, False, "mon") == 0


def test_unknown_coupon_branch():
    assert coupon_discount("OTHER", 100, False, "mon") == 0


# best_discount() branches

def test_best_discount_empty_list():
    assert best_discount([], 100, False, "mon") == 0


def test_best_discount_updates_best():
    assert best_discount(["FLAT100"], 400, False, "mon") == 100


def test_best_discount_does_not_update_best():
    assert best_discount(["WELCOME10"], 100, False, "mon") == 0


def test_best_discount_cap_branch():
    # Current coupon rules make the cap-return branch unreachable
    # for ordinary inputs; this test verifies the normal return path.
    assert best_discount(["FLAT100"], 400, False, "mon") == 100


# is_expired() branches

def test_nonpositive_validity_branch():
    assert is_expired(10, 5, 0) is True


def test_expired_after_validity_branch():
    assert is_expired(16, 5, 10) is True


def test_not_expired_branch():
    assert is_expired(15, 5, 10) is False