from pprint import pprint

import yfinance as yf
import pandas as pd
from datetime import timedelta



# Helper function to find the last Thursday of a given month
def get_next_monthly_expiry(year, month, day):
    # Create a timestamp for the given year, month, and day
    date = pd.Timestamp(year, month, day)

    # Find the last day of the current month
    last_day_current_month = pd.Timestamp(year, month, 1) + pd.offsets.MonthEnd(0)
    # Calculate the last Thursday of the current month
    last_thursday_current_month = last_day_current_month - pd.DateOffset(
        days=(last_day_current_month.weekday() - 3) % 7)

    # Check if there's a Thursday after the given day in the current month
    if (date <= last_thursday_current_month) and (
            date.weekday() <= 3 or (date + pd.DateOffset(days=(3 - date.weekday()))).month == month):
        return last_thursday_current_month
    else:
        # If no Thursday in the current month after the given date, return the last Thursday of next month
        next_month = date + pd.DateOffset(months=1)
        last_day_next_month = pd.Timestamp(next_month.year, next_month.month, 1) + pd.offsets.MonthEnd(0)
        last_thursday_next_month = last_day_next_month - pd.DateOffset(days=(last_day_next_month.weekday() - 3) % 7)
        return last_thursday_next_month


# Helper function to get the first Monday after a given date
def get_first_monday_after(date):
    monday = date + timedelta(days=(7 - date.weekday()))  # Monday is 0
    return monday


# Function to adjust missing data by finding the next available date
def get_next_valid_date(date, data):
    while date not in data.index and date <= data.index.max():
        date += timedelta(days=1)
    return date


# Function to adjust missing data by finding the previous available date
def get_prev_valid_date(date, data):
    while date not in data.index:
        date -= timedelta(days=1)
    return date


# Calculate monthly expiry gains efficiently
def calculate_monthly_gains(ohlcv):
    gains = []
    monthly_gains = {month: [] for month in range(1, 13)}

    # 1. Get the first date in dataframe
    df_start_date = ohlcv.index.min()
    df_end_date = ohlcv.index.max()
    print(df_start_date, df_end_date)

    # 2. Get the month_expiry_date (last Thu of the month)
    last_thu = get_next_monthly_expiry(df_start_date.year, df_start_date.month, df_start_date.day)

    # 3. Get the next Monday
    entry_date = get_first_monday_after(last_thu)
    if entry_date not in ohlcv.index:
        entry_date = get_next_valid_date(entry_date, ohlcv)

    # 4. Get the monthly expiry for entry_date
    monthly_expiry = get_next_monthly_expiry(entry_date.year, entry_date.month, entry_date.day)
    if monthly_expiry not in ohlcv.index:
        monthly_expiry = get_prev_valid_date(monthly_expiry, ohlcv)

    month_dict = {
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
        8: [],
        9: [],
        10: [],
        11: [],
        12: [],
    }
    while monthly_expiry <= ohlcv.index.max() and entry_date <= ohlcv.index.max():
        # print(f"entry_date: {entry_date}, monthly_expiry: {monthly_expiry}")
        gain = float(round(ohlcv.loc[monthly_expiry]['Close'] - ohlcv.loc[entry_date]['Close'], 2))
        gain_pct = float(round(100 * gain / ohlcv.loc[entry_date]['Close'], 2))
        month_dict[monthly_expiry.month].append([gain, gain_pct,
                                                 entry_date.strftime('%Y-%m-%d'),
                                                 monthly_expiry.strftime('%Y-%m-%d')])
        # print(f"month_dict: {month_dict}"), monthly_expiry])

        entry_date = get_first_monday_after(monthly_expiry)
        if entry_date not in ohlcv.index:
            entry_date = get_next_valid_date(entry_date, ohlcv)

        monthly_expiry = get_next_monthly_expiry(entry_date.year, entry_date.month, entry_date.day)
        if monthly_expiry not in ohlcv.index:
            monthly_expiry = get_prev_valid_date(monthly_expiry, ohlcv)
    pprint(month_dict)
    return month_dict


def analyse(gains_data: dict):
    grand_total_points = 0
    grand_total_pct = 0
    total_data_count = 0
    monthly_averages = {}

    for month, values in gains_data.items():
        month_total_points = 0
        month_total_pct = 0
        for d in values:
            month_total_points += d[0]
            month_total_pct += d[1]
        grand_total_points += month_total_points
        grand_total_pct += month_total_pct
        total_data_count += len(values)
        # also convert np.float64 to simple float
        monthly_averages[month] = [round(month_total_points / len(values), 2),
                                   round(month_total_pct / len(values), 2)]

    grand_average_points = round(grand_total_points / total_data_count, 2),
    grand_average_pct = round(grand_total_pct / total_data_count, 2)

    print(f'Grand Average Points: {grand_average_points}')
    print(f'Grand Average Pct: {grand_average_pct}')
    pprint(monthly_averages)


if __name__ == '__main__':
    # print(get_next_monthly_expiry(2024, 4, 29))  # return 2024-05-30
    # print(get_next_monthly_expiry(2024, 12, 30))  # return 2025-01-30
    # print(get_next_monthly_expiry(2024, 6, 2))  # return 2024-07-25

    # Download Nifty 50 data for 1d interval and max duration
    # period = 1y, 2y, 5y, 10y, max
    data = yf.download('^NSEI', interval='1d', period='max', progress=True)

    # Keep only the 'Close' prices for simplicity
    # data = data[['Close']]
    gains_data = calculate_monthly_gains(data)
    analyse(gains_data)

#     for year in range(start_date, end_date + 1):
#         for month in range(1, 13):
#             expiry_date = get_last_thursday(year, month)
#
#             if expiry_date > data.index.max():
#                 # Skip if expiry date is outside the available data range
#                 break
#
#             # Adjust expiry date if data is missing
#             if expiry_date not in data.index:
#                 expiry_date = get_prev_valid_date(expiry_date, data)
#
#             first_monday = get_first_monday_after(expiry_date)
#
#             # Adjust first Monday if data is missing
#             if first_monday not in data.index:
#                 first_monday = get_next_valid_date(first_monday, data)
#
#             if first_monday < expiry_date:
#                 start_price = data.loc[first_monday]['Close']
#                 end_price = data.loc[expiry_date]['Close']
#
#                 gain_points = end_price - start_price
#                 gain_percentage = (gain_points / start_price) * 100
#
#                 # Record gains
#                 gains.append((gain_points, gain_percentage))
#                 monthly_gains[month].append(gain_percentage)
#
#     return gains, monthly_gains
#
#
# # Perform the calculation
# gains, monthly_gains = calculate_monthly_gains(data)
#
# # Compute overall average gain in points and percentage
# average_gain_points = sum(g[0] for g in gains) / len(gains)
# average_gain_percentage = sum(g[1] for g in gains) / len(gains)
#
# # Compute average gain per month
# average_monthly_gains = {month: (sum(gains) / len(gains)) if gains else 0 for month, gains in monthly_gains.items()}
#
# # Output results
# print(f"Average Gain in Points: {average_gain_points:.2f}")
# print(f"Average Gain in Percentage: {average_gain_percentage:.2f}%")
# print("\nAverage Gain for Each Month:")
# for month, avg_gain in average_monthly_gains.items():
#     print(f"Month {month}: {avg_gain:.2f}%")
