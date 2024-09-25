from datetime import datetime, timedelta


def last_thursday_and_next_monday(year: int, month: int, day: int):
    # Find the first day of the next month
    if month == 12:
        first_day_next_month = datetime(year=year + 1, month=1, day=1)
    else:
        first_day_next_month = datetime(year=year, month=month + 1, day=1)

    # Get the last day of the current month
    last_day = first_day_next_month - timedelta(days=1)

    # Find the last Thursday of the month
    last_thursday = last_day
    while last_thursday.weekday() != 3:
        last_thursday -= timedelta(days=1)

    # Find the next Monday after the last Thursday
    next_monday = last_thursday
    while next_monday.weekday() != 0:  # 0 is Monday in Python's datetime
        next_monday += timedelta(days=1)

    # If the next Monday is in the next month, we'll use the first Monday of the next month
    if next_monday.month != last_thursday.month:
        next_monday = first_day_next_month
        while next_monday.weekday() != 0:
            next_monday += timedelta(days=1)

    return last_thursday, next_monday


# # Example usage
# year = 2024
# month = 9  # September
#
# for i in range(1,13):
#     print(f"Month {i}:")
#     last_thurs, next_mon = last_thursday_and_next_monday(year, i)
#     print(f"   Last Thursday of {year}-{i}: {last_thurs.strftime('%Y-%m-%d')}")
#     print(f"   Next Monday after that: {next_mon.strftime('%Y-%m-%d')}")

