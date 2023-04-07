# HH-Muell notification with Telegram
Scrapes the household related "Abholkalender" from "Stadtreinigung Hamburg" and sends a telegram message with all needed informations for the following "Abholung" the day before.

### You have to change YOUR_API_TOKEN token, YOUR_CHAT_ID and your Personal STADTREINIGUNG_URL (e.g. https://www.stadtreinigung.hamburg/abfuhrkalender/?tx_srh_pickups%5Bstreet%5D=4097&tx_srh_pickups%5Bhousenumber%5D=213997&tx_srh_pickups%5BisAllowedOwner%5D=1#c3376) .

This code retrieves information from a website, processes it, and sends a message via Telegram if certain conditions are met. Here is a brief overview of what the code does:

The requests module is used to fetch the HTML content of a webpage, and the BeautifulSoup module is used to parse the HTML and extract the table data from it.
The table data is then processed using regular expressions to replace certain patterns with newlines, commas, or periods as needed.
The resulting message is sent to a specified Telegram chat using the telegram module, but only if tomorrow's date is found in the message.
Overall, this code seems to be well-written and does what it's intended to do. However, there are a few potential issues to keep in mind:

The website being scraped could change its HTML structure, which would break the code's ability to extract the data. It may be worth setting up some sort of error handling or notification system in case this happens.
The regular expressions used to process the data may not be robust enough to handle all possible variations in the input data. Additional testing may be needed to ensure that the code works correctly in all cases.
The use of the telegram module assumes that the user has set up a Telegram bot and obtained an API token and chat ID. This may not be immediately clear to someone unfamiliar with Telegram bot development, so it may be worth including some documentation or comments in the code to explain this.
