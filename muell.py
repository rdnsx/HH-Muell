import asyncio
import requests
from bs4 import BeautifulSoup
import telegram
import re
from datetime import datetime, timedelta
import locale

# Set German locale
locale.setlocale(locale.LC_ALL, 'de_DE.utf8')

# Telegram bot setup
bot = telegram.Bot(token='5732691544:AAEhkYvjp_EhHveVDbNAGMW03QhhpnGwwBs')
chat_id = '-886886289'

async def main():
    # Get the page
    url = 'https://www.stadtreinigung.hamburg/abfuhrkalender/?tx_srh_pickups%5Bstreet%5D=820&tx_srh_pickups%5Bhousenumber%5D=131129&tx_srh_pickups%5BisAllowedOwner%5D=1#c3376'
    page = requests.get(url)

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(page.content, 'html.parser')

    # Find the table
    table = soup.find('table')

    # Extract the information
    rows = table.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        data.append(cols)

    # Replacing certain patterns with newlines
    row_2 = data[1]
    row_2 = [re.sub(r'(.*\d{1,2}\.\s+[A-Za-z]{3}\s+\d{4})', r'\1\n', col) for col in row_2]
    row_2 = [re.sub(r'(alle \d{1,2}\s+[A-Za-z]+)', r'\1\n', col) for col in row_2]
    row_2 = [re.sub(r'alle 4 Wochen', ',', col) for col in row_2]
    row_2 = [re.sub(r'14-täglich', ',', col) for col in row_2]
    row_2 = [re.sub(r'1 x wöchentlich', ',', col) for col in row_2]
    message = ' '.join(row_2)
    message = re.sub(r'\s+', ' ', message)  # Removing extra spaces
    message = re.sub(r'(\d{4})', r'\1\n\n', message)  # insert new line after year
    # Replacing last comma with period
    if message[-1] == ',':
        message = message[:-1] + '.'

    # Sending the message
    tomorrow = datetime.now() + timedelta(days=1)
    date_str = tomorrow.strftime('%d. %B %Y')
    if date_str in message:
        sent_message = bot.send_message(chat_id=chat_id, text=message)
        if sent_message:
            print("Message sent successfully.")
        else:
            print("Message sending failed.")
    else:
        print(f"Date '{date_str}' not found in message. Message not sent.")

if __name__ == '__main__':
    asyncio.run(main())
