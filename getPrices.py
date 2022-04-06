import yfinance as yf

cache = {}
def getPrice(ticker):


	if ticker in cache:
		print("Returning chached price")
		return cache[ticker]
	
	print('fetching stock price')
	stock = yf.Ticker(ticker)
	info = stock.info
	price = info['regularMarketPrice']
	cache[ticker] = price

	return price


def main():

	print(getPrice('ATEC.AX'))
	print(getPrice('ATEC.AX'))

if __name__ == '__main__':

	main()