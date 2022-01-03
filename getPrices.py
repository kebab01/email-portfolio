import yfinance as yf

def getPrice(ticker):

	stock = yf.Ticker(ticker)

	info = stock.info

	price = info['regularMarketPrice']

	return price


def main():

	print(getPrice('1MC.AX'))

if __name__ == '__main__':

	main()