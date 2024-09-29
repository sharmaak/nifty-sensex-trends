# Script to check how nifty and sensex behaved on equinox and solstice days.
from datetime import datetime

import yfinance as yf
from pandas import DataFrame


def calc_gain(df: DataFrame, date: datetime):
    if date not in df.index:
        return 'NA'

    iloc_index = df.index.get_loc(date)
    gain_pct = 100*(df.iloc[iloc_index]['Close'] - df.iloc[iloc_index-1]['Close'])/df.iloc[iloc_index-1]['Close']
    gain_pct = round(gain_pct, 2)
    return gain_pct


if __name__ == '__main__':
    # 1. Get the data for sensex as much back as possible
    df = yf.download('^BSESN', interval='1d', period='max', progress=True)
    df_start_date = df.index.min()
    df_end_date = df.index.max()
    print(f"start: {df_start_date} | end: {df_end_date}")

    # March 21 (Vernal equinox)
    # September 23 (Autumnal equinox)
    # June 21(Summer Solstice)
    # Dec 22 (Winter Solstice)

    data = []
    for y in range(df_start_date.year, df_end_date.year+1):
        print(f"Processing year {y}")
        vernal_equinox   = datetime(year=y, month=3, day=21)
        autumnal_equinox = datetime(year=y, month=9, day=23)
        summer_solstice  = datetime(year=y, month=6, day=21)
        winter_solstice  = datetime(year=y, month=12, day=22)

        # calculate gains on these days
        eqnx_2103 = calc_gain(df, vernal_equinox)
        slst_2106 = calc_gain(df, summer_solstice)
        eqnx_2309 = calc_gain(df, autumnal_equinox)
        slst_2212 = calc_gain(df, winter_solstice)
        data.append([y, eqnx_2103, slst_2106, eqnx_2309, slst_2212])
    spl_df = DataFrame(columns=["Year", "21 Mar", "21 Jun", "23 Sep", "22 Dec"], data=data)
    print(spl_df.to_string())
    # Pure bullshit! Run and see for yourself. There is no clearcut pattern of
    # gains or losses on equinoxes and solstices. Crazy things people say.

