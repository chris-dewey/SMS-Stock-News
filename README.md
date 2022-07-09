# SMS-Stock-News
Monitor stock prices. A daily change over 5% will trigger a text message containing the percent change and two news articles.

The main.py file also contains the instructions below. Enjoy.

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
