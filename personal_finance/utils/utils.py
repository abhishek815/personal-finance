def determine_month(month: int):
    if month >= 1 and month < 10:
        return f"0{month}"
    elif month >= 10 and month <= 12:
        return month
    else:
        raise Exception("Invalid month value, please enter a value between 1 and 12")
