"""
Monitor your favorite stocks. If the difference between prices from last close and the previous close is greater than
5%, receive a text message with the percentage change and the two most recent articles about the company.

*** SETUP ***
Step 1: Sign up and retrieve your credentials for the following:
    Stocks: www.alphavantage.co (API Key)
    Text Messages: www.twilio.com (Note: 3 items needed, SID, Authentication Token, and your Twilio Phone Number)
    News: www.newsapi.org (API Key)
    Link Shortener: www.bit.ly (Token)

Step 2: Modify Configuration Variables
    a. Add the above information to the VARIABLES section below.
    b. Enter your phone number that will receive the text messages with the format "+11234567890"
    c. Modify the STOCKS variable with stocks you wish to follow with the example below.

Step 3: Setup Automatic Runtime
To enable automatic alerts, this application can be set up to execute once per day at market close with many online
services, such as AWS lambda or PythonAnywhere.
"""

import requests
from twilio.rest import Client

# ---------- MODIFY THESE VARIABLES IN SETUP ---------- #
STOCKS = [("TSLA", "tesla"), ("MSFT", "microsoft")]
STOCK_API_KEY = "your stock api key here"
NEWS_API_KEY = "your news api key here"
TWILIO_SID = "your twilio sid here"
TWILIO_AUTH = "your twilio authentication token here"
TWILIO_PH = "your twilio phone number here"
BITLY_TOKEN = "your bit.ly token here"
MY_PHONE_NUMBER = "your personal phone number here"
# ----------------------------------------------------- #


def get_stock_data(stock: str) -> dict:
    """
    Gets the two most recent close prices and calculates percentage change.
    Parses JSON data from API call to alphavantage.co

    :param stock: Stock Ticker Symbol
    :return: recent_close, previous_close, change
    """
    endpoint = "https://www.alphavantage.co/query"
    params = {"function": "TIME_SERIES_DAILY", "symbol": stock, "apikey": STOCK_API_KEY}
    try:
        stock_data = [value for key, value in (requests.get(endpoint, params=params).json()["Time Series (Daily)"]).items()]
        most_recent, previous = float(stock_data[0]["4. close"]), float(stock_data[1]["4. close"])
        change = ((previous - most_recent) / previous) * 100
        return {"recent_close": most_recent, "previous_close": previous, "change": round(change, 1)}
    except KeyError:
        return {"recent_close": 0, "previous_close": 0, "change": 0}


def get_news(query: str) -> list[str]:
    """
    Get most recent news article about a company.
    Parses JSON data from API call to newsapi.org

    :param query: Find articles matching this keyword (company name)
    :return: Articles and their URLs
    """
    endpoint = "https://newsapi.org/v2/everything"
    params = {"q": query, "sortBy": "publishedAt", "language": "en", "apiKey": NEWS_API_KEY}
    news_data = requests.get(endpoint, params=params).json()["articles"][:2]

    return [f"{article['title']}\n{shorten_link(article['url'])}" for article in news_data]


def send_text(message: str):
    """
    Send text message using Twilio API
    :param message: text message to be sent
    """
    client = Client(TWILIO_SID, TWILIO_AUTH)
    msg = client.messages.create(body=message, from_=TWILIO_PH, to=MY_PHONE_NUMBER)


def shorten_link(url: str):
    bitly_endpoint = "https://api-ssl.bitly.com/v4/shorten"
    headers = { 'Authorization': BITLY_TOKEN, 'Content-Type': 'application/json' }
    data = '{ "long_url": ' + f"\"{url}\"" + ' }'

    return requests.post(bitly_endpoint, headers=headers, data=data).json()['link']


# ---------- MAIN LOGIC ---------- #
for ticker, company in STOCKS:
    stock_info = get_stock_data(ticker)
    if abs(stock_info["change"]) > 5:
        arrow = "🔻" if stock_info['change'] < 0 else "🔺"
        news = get_news(company)
        if news:
            news_info = ""
            for item in news:
                news_info += item + "\n"
            message_content = f"{ticker.upper()}: {arrow} {abs(stock_info['change'])}%\n{news_info}"
            send_text(message_content)
