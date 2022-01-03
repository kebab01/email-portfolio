import smtplib 
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import locale
from dotenv import load_dotenv
load_dotenv()

locale.setlocale(locale.LC_ALL, '' )# Set currency location

EmailAddy = os.getenv("EMAIL") #senders Gmail id here
Pass = os.getenv("EMAIL_PASS") #senders Gmail's Password over here 

def getDate():

    now = datetime.datetime.now()
    now = now.strftime("%d/%m/%Y")
    return now

def sendEmail(contentHTML, contentPLAIN, recipient):

    msg = MIMEMultipart("alternative")
    msg['Subject'] = "Weekly portfolio value"
    msg['From'] = EmailAddy
    msg['To'] = recipient
    #Generate mail attachment
    part1 = MIMEText(contentPLAIN, "plain")
    part2 = MIMEText(contentHTML, "html")
    #Attach mail
    msg.attach(part1)
    msg.attach(part2)

    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp: #Added Gmails SMTP Server
        smtp.login(EmailAddy,Pass)
        smtp.sendmail(EmailAddy, recipient, msg.as_string())
        smtp.quit()
        print("Email sent to", recipient)
        del msg['To']
        del msg['From']
        del msg['Subject']

def email(person):

    recipient = person.getEmail()
    subject = "Weekly summary"
    contentHTML, contentPLAIN = generateContent(person)

    sendEmail(contentHTML, contentPLAIN, recipient)

def generateContent(person):
    print("Generating email...")
    #If html doesnt load this is displayed
    text = "an error occured"

    #open templates
    template = open("template.html").read()
    rowTemplate1 = open("rows1.html").read() # Rows for weekly summary
    rowTemplate2 = open("rows2.html").read() # rows for weekly comparison

    rows1 = ""
    rows2 = ""
    stocks = person.getStocks()
    #Generate rows for template and put them together
    for stock in stocks:

        #Replace for weekly summary
        row1 = rowTemplate1.replace("//stock//", stock.getTicker())
        row1 = row1.replace("//units//", str(stock.getQuantity()))
        row1 = row1.replace("//price//", locale.currency(stock.getLatestPrice(), grouping=True))
        row1 = row1.replace("//value//", locale.currency(stock.getLatestPrice() * stock.getQuantity(),grouping=True))

        #Replace for weekly comparison
        row2 = rowTemplate2.replace("//stock//", stock.getTicker())
        row2 = row2.replace("//at_purchase//", locale.currency(stock.getPurchasePrice() * stock.getQuantity(),grouping=True))
        row2 = row2.replace("//last_week//", locale.currency(stock.getPreviousPrice() * stock.getQuantity(),grouping=True))
        row2 = row2.replace("//this_week//", locale.currency(stock.getLatestPrice() * stock.getQuantity(), grouping=True))

        #If no data for purchase price or previous week price handle devision by zero error
        try:
            row2 = row2.replace("//over_purchase//", str(round(((stock.getLatestPrice()/stock.getPurchasePrice())-1)*100,2)))
        except ZeroDivisionError:
            row2 = row2.replace("//over_purchase//", str("No data"))

        try:
            row2 = row2.replace("//over_week//", str(round((((stock.getLatestPrice()/stock.getPreviousPrice()))-1)*100, 2)))
        except ZeroDivisionError:
            row2 = row2.replace("//over_week//", str("No data"))

        rows1 += row1 + "\n"
        rows2 += row2 + "\n"

    #Add portfolio info to button of weekly tracker 
    rows2 += addPortfolioInfo(person, rowTemplate2)

    #format email and put row templates in email
    html = open("template.html").read()
    html = html.replace("//name//", person.getName())
    html = html.replace("//date//", str(getDate()))
    html = html.replace("//insertRows1//", rows1)
    html = html.replace("//insertRows2//", rows2)
    html = html.replace("//total//", locale.currency(person.getLatestNet(),grouping=True))

    return html, text

def addPortfolioInfo(person, template):

    row2 = template.replace("//stock//", "Portfolio Value")
    row2 = row2.replace("//at_purchase//", locale.currency(person.getPurchaseNet(), grouping=True))
    row2 = row2.replace("//last_week//", locale.currency(person.getPreviousNet(), grouping=True))
    row2 = row2.replace("//this_week//", locale.currency(person.getLatestNet(),grouping=True))

    # Handle division by zero
    try:
        row2 = row2.replace("//over_purchase//", str(round(((person.getLatestNet()/person.getPurchaseNet())-1)*100,2)))
    except ZeroDivisionError:
        row2 = row2.replace("//over_purchase//", str("No data"))

    try:
        row2 = row2.replace("//over_week//", str(round(((person.getLatestNet()/person.getPreviousNet())-1)*100,2)))
    except ZeroDivisionError:
        row2 = row2.replace("//over_week//", str("No data"))

    return row2





