# Muell notification with Telegram
Scrapes the household related "Abholkalender" from "Stadtreinigung Hamburg" and sends a telegram message with all needed informations for the following "Abholung".

This is a Python script that scrapes a webpage and sends a message containing the scraped data to a Telegram chat using a bot API token and chat ID. Here's a brief overview of what the script does:

Imports the necessary modules: asyncio, requests, BeautifulSoup for web scraping, and telegram for sending messages through Telegram.
Defines the Telegram bot API token and chat ID variables.
Defines an async function called main().
Uses the requests module to fetch the HTML content of a webpage at a given URL.
Uses BeautifulSoup to parse the HTML content and extract a table from it.
Extracts the data from the table and applies some text formatting to it using regular expressions.
Constructs a message from the formatted data and sends it to the specified Telegram chat using the telegram module.
Prints a success or failure message depending on whether the message was sent successfully or not.
Finally, the script runs the main() function using asyncio.run().

Note that in order to use this script, you will need to replace the YOUR_API_TOKEN and YOUR_CHAT_ID placeholders with your own Telegram bot API token and chat ID, respectively.