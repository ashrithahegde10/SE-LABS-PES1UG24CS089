
from datetime import datetime, date
import math


def split_code(code):
    if not isinstance(code, str):
        return None

    parts = code.strip().upper().split('-')

    if len(parts) != 2:
        return None

    prefix, value = parts

    if not prefix or not value:
        return None

    try:
        number = int(value)
    except ValueError:
        return None

    return prefix, number


def most_expensive(prices_csv):
    if not isinstance(prices_csv, str):
        return None

    price_strings = prices_csv.split(',')

    if not price_strings or any(not p.strip() for p in price_strings):
        return None

    try:
        prices = [float(p.strip()) for p in price_strings]
    except ValueError:
        return None

    if not all(math.isfinite(p) for p in prices):
        return None

    return max(prices)


def expiry_days(date_text):
    if not isinstance(date_text, str):
        return None

    try:
        parsed_date = datetime.strptime(
            date_text.strip(), "%Y-%m-%d"
        ).date()

        # Ensure the input follows the exact YYYY-MM-DD format.
        if parsed_date.isoformat() != date_text.strip():
            return None

    except ValueError:
        return None

    reference_date = date(2024, 1, 1)
    return (parsed_date - reference_date).days


def main():
    print("==== Running split_code ====")
    user_input = input("Enter a coupon code (e.g. save-20): ")
    result = split_code(user_input)
    print("Prefix and Value:", result)

    print("\n==== Running most_expensive ====")
    user_input = input("Enter item prices as CSV (e.g. 199,49.5,320): ")
    result = most_expensive(user_input)
    print("Most Expensive Item:", result)

    print("\n==== Running expiry_days ====")
    user_input = input("Enter an expiry date as YYYY-MM-DD: ")
    result = expiry_days(user_input)
    print("Days Since 2024:", result)


if __name__ == "__main__":
    main()
