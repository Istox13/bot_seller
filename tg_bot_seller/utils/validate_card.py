def validate_card(card_number: str) -> bool:
    """Провека контрольной суммы номера карты по формуле Луна"""

    card_number = card_number.replace(" ", "")
    check_digit = 0

    if len(card_number) != 16:
        return False

    for i, digit in enumerate(card_number):
        digit = int(digit)

        if i % 2 == 0:
            digit *= 2

            if digit > 9:
                digit -= 9

        check_digit += digit

    return check_digit % 10 == 0
