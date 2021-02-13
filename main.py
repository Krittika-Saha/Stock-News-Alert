from requests import get
STOCK = "TSLA"
COMPANY_NAME = "Tesla%20Inc"
from datetime import datetime, timedelta
from twilio.rest import Client

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "_YOUR_API_KEY_"
NEWS_API_KEY = "_YOUR_API_KEY_"
account_sid = "_YOUR_SID_"
auth_token = '_YOUR_API_KEY_'
string = ""


## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
#HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = 20.
#HINT 2: Work out the value of 5% of yerstday's closing stock price.

stock_response = get(f"{STOCK_ENDPOINT}?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey={STOCK_API_KEY}")
stock_response.raise_for_status()
stock_data = stock_response.json()
closing_price_yesterday = float(stock_data['Time Series (Daily)'][f"{str(datetime.today() - timedelta(days = 1))[:10]}"]['4. close'])
closing_price_before_yesterday = float(stock_data['Time Series (Daily)'][f"{str(datetime.today() - timedelta(days = 2))[:10]}"]['4. close'])
difference = closing_price_yesterday - closing_price_before_yesterday
diff_percent = (abs(difference)/closing_price_yesterday) * 100
if difference < 0:
    string = f"🔻{round(diff_percent, 2)}%"
else:
    string = f"🔺{round(diff_percent, 2)}%"


## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number. 
#HINT 1: Consider using a List Comprehension.
if diff_percent > 5:
    news_data = (get(f"{NEWS_ENDPOINT}?q={COMPANY_NAME}&apiKey={NEWS_API_KEY}").json())['articles'][:3]
    client = Client(account_sid, auth_token)
    for i in range(len(news_data)):
        message = client.messages.create(
            body=f"""
           {STOCK}:  {string}
Headline: {news_data[i]['title']} ({STOCK})?
Brief: {news_data[i]['description']}""",
            from_='whatsapp:+_YOUR_SANDBOX_PHONE_',
            to='whatsapp:+_YOUR_PHONE_'
        )
        print(message.status)


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

