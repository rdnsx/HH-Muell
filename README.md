# HH-Muell notification with Telegram
Scrapes the household related "Abholkalender" from "Stadtreinigung Hamburg" and sends a telegram message with all needed informations for the following "Abholung" the day before.
Screenshot_2023-04-07-21-30-53-550-edit_com.miui.gallery.jpg

This code retrieves information from the website, processes it, and sends a message via Telegram if certain conditions are met. Here is a brief overview of what the code does:

The requests module is used to fetch the HTML content of the webpage, and the BeautifulSoup module is used to parse the HTML and extract the table data from it.
The table data is then processed using regular expressions to replace certain patterns with newlines, commas, or periods as needed.
The resulting message is sent to a specified Telegram chat using the telegram module, but only if tomorrow's date is found in the message.

## How to setup Telegram... 

Create a Telegram bot by talking to the BotFather. Follow the instructions provided by the BotFather to create a new bot and obtain an API token.

Get your chat ID by sending a message to your bot and then using the following URL in your web browser:

https://api.telegram.org/bot<YOUR_API_TOKEN>/getUpdates

Replace <YOUR_API_TOKEN> with your actual API token. This URL will return a JSON response that contains information about your bot's recent messages. Look for the chat object that corresponds to the chat where you sent the message. The id field of the chat object is your chat ID.

Replace the YOUR_API_TOKEN and YOUR_CHAT_ID placeholders in the script with your actual API token and chat ID.

Replace the STADTREINIGUNG_URL placeholder with your Individual URL from the Stadtreinigung.

e.g. https://www.stadtreinigung.hamburg/abfuhrkalender/?tx_srh_pickups%5Bstreet%5D=4097&tx_srh_pickups%5Bhousenumber%5D=213997&tx_srh_pickups%5BisAllowedOwner%5D=1#c3376

### If you'd build and run it as a docker container you can also include environment variables in the Docker run command:

docker run --rm -e API_TOKEN=your_api_token -e CHAT_ID=your_chat_id -e STADTREINIGUNG_URL=your_stadtreinigung_url <image-name>

