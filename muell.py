import asyncio
import requests
from bs4 import BeautifulSoup
import telegram
import re
from datetime import datetime, timedelta
import locale
import os

# Set German locale
locale.setlocale(locale.LC_ALL, 'de_DE.utf8')

# Telegram bot setup
token = os.getenv('YOUR_BOT_TOKEN')
chat_id = os.getenv('YOUR_CHAT_ID')
url = os.getenv('URL_STADTREINIGUNG')

# Validate environment variables
if not token:
    raise ValueError("YOUR_BOT_TOKEN environment variable is not set")
if not chat_id:
    raise ValueError("YOUR_CHAT_ID environment variable is not set")
if not url:
    raise ValueError("URL_STADTREINIGUNG environment variable is not set")

print(f"Initializing bot with token: {token[:5]}...{token[-5:]}")
print(f"Chat ID: {chat_id}")
print(f"URL: {url}")

bot = telegram.Bot(token=token)

async def main():
    try:
        # Get the page
        print(f"Fetching data from URL: {url}")
        page = requests.get(url)
        page.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the page with BeautifulSoup
        print("Parsing HTML content")
        soup = BeautifulSoup(page.content, 'html.parser')

        # Find the table
        table = soup.find('table')
        if not table:
            raise ValueError("Could not find table in HTML content")

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
        print(f"Checking if tomorrow's date ({date_str}) is in the message")
        
        if date_str in message:
            print("Date found in message. Sending Telegram notification...")
            try:
                sent_message = await bot.send_message(chat_id=chat_id, text=message)
                if sent_message:
                    print("Message sent successfully.")
                else:
                    print("Message sending failed.")
            except Exception as e:
                print(f"Error sending Telegram message: {e}")
                raise
        else:
            print(f"Date '{date_str}' not found in message. Message not sent.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from URL: {e}")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

if __name__ == '__main__':
    asyncio.run(main())
