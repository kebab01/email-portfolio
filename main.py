from ast import arg
import json
import getPrices
import datetime
import locale
from mail import sendEmail
from jinja2 import Environment, FileSystemLoader
import argparse

locale.setlocale(locale.LC_ALL, '' )# Set currency location

def updateHoldings(holdings):

	for holding in holdings:
		print("getting price for stock")

		latestPrice = getPrices.getPrice(f"{holding['ticker']}.AX")
		holding['recent-price'] = latestPrice
		holding['history'].append({
			"time":datetime.datetime.now().isoformat(),
			"price":latestPrice
		})

	return holdings

def generateHTML(person):
	print('Doing calculations for email...')

	date = datetime.datetime.now()
	date = date.strftime("%-d %B %Y")

	print("Generating email...")

	file_loader = FileSystemLoader("templates")
	env = Environment(loader=file_loader)
	template = env.get_template('email.html')

	return template.render(
		date=date, 
		netPurchase=round(sum(i['purchase-price'] for i in person['holdings']),2),
		netRecent=round(sum(i['recent-price'] for i in person['holdings']),2),
		netLastWeek=round(sum(i['history'][-2]['price'] for i in person['holdings']),2),
		person=person, 
		calcPercent=calcPercent
		)

def calcPercent(x, y):

	try:
		return round(((x/y) - 1)*100,2)
	except ZeroDivisionError:
		return 0

def main():

	parser = argparse.ArgumentParser(description='Manage portfolio tracking')
	parser.add_argument('-a', help="Add new holding", action="store_true")
	args = vars(parser.parse_args())

	data = open('data.json').read()
	persons = json.loads(data)

	if args['a'] == False:
		
		updatedPersons = []
		for person in persons:
			print("Getting info for", person['name'])
			#Update stock prices
			person['holdings'] = updateHoldings(person['holdings'])
			content = generateHTML(person)

			sendEmail(subject="Weekly Portfolio Update",recipient=person['email'], content=content)
			updatedPersons.append(person)

		with open('data.json','w') as f:
			json.dump(updatedPersons,fp=f, indent=2)

if __name__ == "__main__":
	main()