def is_positive_number(valueInput):
    try:
        number_string = float(valueInput)
    except (ValueError, TypeError):
        # print(e)
        return False
    return number_string > 0
