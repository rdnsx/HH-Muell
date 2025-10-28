import asyncio
import requests
from bs4 import BeautifulSoup
import telegram
import re
from datetime import datetime, timedelta
import locale
import os

# Set German locale
try:
    locale.setlocale(locale.LC_ALL, 'de_DE.utf8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
    except locale.Error:
        print("Warning: Could not set German locale. Using manual month mapping.")

# German month names mapping to ensure consistency
GERMAN_MONTHS = {
    1: 'Januar',
    2: 'Februar', 
    3: 'März',
    4: 'April',
    5: 'Mai',
    6: 'Juni',
    7: 'Juli',
    8: 'August',
    9: 'September',
    10: 'Oktober',
    11: 'November',
    12: 'Dezember'
}

# English month names mapping (for website compatibility)
ENGLISH_MONTHS = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

def format_german_date(date_obj):
    """Format date with German month names"""
    day = date_obj.day
    month = GERMAN_MONTHS[date_obj.month]
    year = date_obj.year
    return f"{day}. {month} {year}"

def format_english_date(date_obj):
    """Format date with English month names"""
    day = date_obj.day
    month = ENGLISH_MONTHS[date_obj.month]
    year = date_obj.year
    return f"{day}. {month} {year}"

def get_date_variants(date_obj):
    """Get both German and English date formats for checking"""
    return [format_german_date(date_obj), format_english_date(date_obj)]

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

        # Check for tomorrow's date
        tomorrow = datetime.now() + timedelta(days=1)
        date_variants = get_date_variants(tomorrow)
        print(f"Looking for tomorrow's date in table. Variants: {date_variants}")
        
        # Search through all rows to find tomorrow's date
        date_found = False
        found_date = None
        message = None
        
        for i, row_data in enumerate(data):
            if not row_data or len(row_data) == 0:
                continue
                
            # Join the row to check if tomorrow's date is in it
            row_text = ' '.join(row_data)
            
            # Check if any date variant is in this row
            for date_str in date_variants:
                if date_str in row_text:
                    print(f"Found tomorrow's date in row {i}: {row_data}")
                    date_found = True
                    found_date = date_str
                    
                    # Process this row to create the message
                    row_processed = row_data.copy()
                    row_processed = [re.sub(r'(.*\d{1,2}\.\s+[A-Za-z]+\s+\d{4})', r'\1\n', col) for col in row_processed]
                    row_processed = [re.sub(r'(alle \d{1,2}\s+[A-Za-z]+)', r'\1\n', col) for col in row_processed]
                    row_processed = [re.sub(r'alle 4 Wochen', ',', col) for col in row_processed]
                    row_processed = [re.sub(r'14-täglich', ',', col) for col in row_processed]
                    row_processed = [re.sub(r'1 x wöchentlich', ',', col) for col in row_processed]
                    message = ' '.join(row_processed)
                    message = re.sub(r'\s+', ' ', message)  # Removing extra spaces
                    message = re.sub(r'(\d{4})', r'\1\n\n', message)  # insert new line after year
                    # Replacing last comma with period
                    if message and message[-1] == ',':
                        message = message[:-1] + '.'
                    break
            
            if date_found:
                break
        
        if date_found:
            print(f"Date found in message: '{found_date}'. Sending Telegram notification...")
            try:
                sent_message = bot.send_message(chat_id=chat_id, text=message)
                if sent_message:
                    print("Message sent successfully.")
                else:
                    print("Message sending failed.")
            except Exception as e:
                print(f"Error sending Telegram message: {e}")
                raise
        else:
            print(f"None of the date variants {date_variants} found in message. Message not sent.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from URL: {e}")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

if __name__ == '__main__':
    asyncio.run(main())
