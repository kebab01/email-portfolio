import mail
import getPrices
import datetime
import pickle
import os 
import sys
from dotenv import load_dotenv
load_dotenv()

# contains infomation about person what stocks they own and what those stocks are worth
class PersonObj:

	stocks = []
	purchaseNet = 0
	lastWeeksNet = 0
	thisWeeksNet = 0

	def __init__(self, name, email, stocks):
		self.name = name
		self.email = email
		self.stocks = stocks 
		self.purchaseNet = self.calcPurchaseNet()

	def getStocks(self):
		return self.stocks

	def getStockTickers(self):
		tickers = []
		for stock in self.stocks:
			tickers.append(stock.getTicker())

	def getName(self):
		return self.name

	def getEmail(self):
		return self.email

	def calcPurchaseNet(self):
		total = 0
		for stock in self.stocks:
			total += stock.getPurchasePrice() * stock.getQuantity()

		return total

	def calcNetWorth(self):

		total = 0
		for stock in self.stocks:
			total += stock.getLatestPrice() * stock.getQuantity()

		return total

	def getPreviousNet(self):
		return self.lastWeeksNet

	def getLatestNet(self):
		return self.thisWeeksNet

	def getPurchaseNet(self):
		return self.purchaseNet

	def addPurchase(self, ticker, quantity, purchasePrice):
		self.stocks.append(stockClass(ticker,purchasePrice, quantity))

	def update(self):
		self.lastWeeksNet = self.thisWeeksNet
		self.thisWeeksNet = self.calcNetWorth()

	def toString(self):
		print(self.name, self.email, self.stocks, self.portfolio)

class stockClass:

	ticker = str()
	purchasePrice = 0
	lastWeekPrice = 0
	thisWeekPrice = 0
	quantity = 0

	def __init__(self, ticker, purchasePrice, quantity):
		self.ticker = ticker
		self.purchasePrice = purchasePrice
		self.quantity = quantity

	def getTicker(self):
		return self.ticker;

	def setPurchase(self, price):
		self.purchasePrice = price

	def setPreviousPrice(self, price):
		self.lastWeekPrice = price

	def setLatestPrice(self,price):
		self.thisWeekPrice = price

	def getLatestPrice(self):
		return self.thisWeekPrice;

	def getPreviousPrice(self):
		return self.lastWeekPrice

	def getPurchasePrice(self):
		return self.purchasePrice

	def getQuantity(self):
		return self.quantity

	def update(self):
		#Update stock price info
		print(f"Updating stock price for {self.ticker}")
		self.lastWeekPrice = self.thisWeekPrice
		self.thisWeekPrice = getPrices.getPrice(self.ticker + ".AX")

	def toString(self):
		print(self.ticker, self.purchasePrice, self.lastWeekPrice, self.thisWeekPrice)


people = [] #Array of person objects

def getTime():
	now = datetime.datetime.now()
	now = now.strftime("%H:%m:%s %d-%m-%Y")

	return now

def export():

	people.append(PersonObj('Person1', 'person1@domain.com', [stockClass('AJM',94.12, 2.5553), stockClass('DCX',14.2100, 17.4427)]))
	people.append(PersonObj('Person2', 'person2@domain.com', [stockClass('AJM',94.12, 10.2212), stockClass('DCX',14.2100, 69.7708)]))
	people.append(PersonObj('Person3', "person3@domain.com", [stockClass('AJM',94.12, 10.2212), stockClass('DCX',14.2100, 69.7708), stockClass('CWL',22.3200,45), stockClass('ANL',15.9400,141)]))
	
	for person in people:

		savePerson(person)

def addPurchase():
	#Add a purchase to user profile
	names = ["Person1", "Person2", "Person3"]

	for name in names:
		with open(name + ".dat", "rb") as f:
			person = pickle.load(f)
			people.append(person)

	flag = False
	selectedPerson = ""

	while flag == False:

		userInput = str(input("Enter name to add purchase to: "))
		flag, selectedPerson = getValid(userInput)

	while True:
		ticker = input("Enter stock ticker: ")
		print("Checking ticker is valid...")
		price = getPrices.getPrice(ticker + ".AX")
		if price != None:
			break
		else:
			print("invalid ticker")

	while True:
		try:
			quantity = float(input("Enter quantity: "))
			purchasePrice = float(input("Enter purchase price: "))
			break

		except ValueError:
			print("Invalid entry, try again")

	selectedPerson.addPurchase(ticker, quantity, purchasePrice)
	savePerson(selectedPerson)
	print("Purchase added to "+ selectedPerson.getName())

def getValid(userInput):

	for person in people:
		if userInput in person.getName():
			return True, person

	print("User does not exist")
	return False, None

def updatePerson():
	#update person object, includes updateing of stock prices person owns
	print("loading")
	names = ["Person1", "Person2", "Person3"]

	for name in names:
		with open(name + ".dat", "rb") as f:
			person = pickle.load(f)
			people.append(person)

			#Update their stock prices
			for stock in person.getStocks():
				stock.update()
				stock.toString();

			person.update()

	for person in people:
		savePerson(person)

def savePerson(person):
	with open(person.getName() + ".dat", "wb") as f:
			pickle.dump(person, f)

def main():

	if len(sys.argv) == 2:

		print(getTime())
		print("Calculating holdings..")

		if sys.argv[1] == "-a":
			addPurchase()

		elif sys.argv[1] == "-n":
			updatePerson()
			for person in people:
				mail.email(person)
		elif sys.argv[1] == "-e":
			export()

		else:
			print("Invalid option \nChose either: \n-n for normal use  \n-a to add a purcchase \n-e to re export person objects")
	
	else:
		print("Invalid arguments")

if __name__ == "__main__":

	# main()
	print(os.getenv("PASS"))

