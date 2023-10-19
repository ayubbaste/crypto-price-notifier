import os
import requests
import json
from dotenv import load_dotenv
from datetime import date, datetime, timedelta

# take environment variables from .env
# pip install python-binance
# https://python-binance.readthedocs.io/en/latest/overview.html
load_dotenv() 

# Telegram
from pyrogram import Client
# For Telegram
session_name = os.getenv('SESSION_NAME')
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
recipients = [os.getenv('RECIPIENTS')]


totrack = [
    {
        "asset": "SOLUSDT",
        "rule": ">=",
        "track_price": 100000
    },
    {
        "asset": "XRPUSDT",
        "rule": "<=",
        "track_price": 100000
    },
]

while True:
    messages = [] 

    if totrack:
        # track coins and there prices
        for val in totrack:
            data = requests.get("https://api.binance.com/api/v3/ticker/price?symbol={}".format(val["asset"])).text
            current_price = float(json.loads(data)['price'])

            if val["rule"] == "<=":
                if current_price <= val["track_price"]:
                    now = datetime.now()
                    timestamp = now.strftime("%d-%m-%Y %H:%M")

                    new_message = "{0} {1} / {2}".format(val["asset"], current_price, timestamp)
                    messages.append(new_message)
                    totrack.remove(val)

            elif val["rule"] == ">=":
                if current_price >= val["track_price"]:
                    now = datetime.now()
                    timestamp = now.strftime("%d-%m-%Y %H:%M")

                    new_message = "{0} {1} / {2}".format(val["asset"], current_price, timestamp)
                    messages.append(new_message)
                    totrack.remove(val)

    # If there is a new vacancies
    if len(messages) > 0:
        for i in messages:
            print(i)
        try:
            app = Client(
                session_name,
                api_id = int(api_id),
                api_hash = api_hash,
                bot_token = bot_token
            )

            # Send them with telegram
            for message in messages:

                async def main():
                    async with app:
                        for recipient in recipients:
                            await app.send_message(int(recipient), message, parse_mode="html", disable_web_page_preview = True)
                app.run(main())
        except:
            pass

