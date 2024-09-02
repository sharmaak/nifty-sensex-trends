import yfinance as yf
from pprint import pprint

def dig(index: str, duration_in_years: int):
	
	period = 'max' if duration_in_years <= 0 else f'{duration_in_years}y'
	data = yf.download(index, interval='1mo', period=period, progress=False)
	print(f"Period: {period} | Start Date: {data.index[0].strftime('%d-%m-%y')} | End Date: {data.index[len(data)-1].strftime('%d-%m-%y')}")

	# 1. Calculate monthly average gain in points and percentage
	data['Monthly_Gain'] = data['Close'] - data['Open']
	average_monthly_gain = data['Monthly_Gain'].mean()
	print(f"average_monthly_gain: {round(average_monthly_gain,2)}")

	# 2. Now we want to find that on an average for each month, what was the average gain across years? 
	book = {}
	for i in range(1,13):
		book.update({"{:02d}".format(i): []})

	for i in range(0, len(data)):
		month = data.index[i].strftime('%m')
		gain = round(float(data['Monthly_Gain'].iloc[i]), 2)
		book[month].append(gain)

	print('Month, Loss Ratio, Average Gain')
	for m in book.keys():
		month_gain_values = book[m]
		
		average_gain = sum(month_gain_values) / len(month_gain_values)

		gain_count = 0
		loss_count = 0
		for v in month_gain_values:
			if v > 0: 
				gain_count = gain_count + 1
			else:
				loss_count = loss_count + 1
		profit_ratio = gain_count / (gain_count + loss_count)
		print(f"{m}, \"{loss_count}/{(gain_count + loss_count)}\", {round(average_gain, 2)}")
	print('-----------------')


if __name__ == '__main__':
	# period must be one of ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']")
	BSE='^BSESN'
	NSE='^NSEI'
	index=BSE
	dig(index, 2)
	dig(index, 5)
	dig(index, 10)
	dig(index, -1)
