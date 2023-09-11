# SeekingAlpha News Bot for Discord

This bot is designed to scrape the latest market news from SeekingAlpha and post it in a specified Discord channel every 5 minutes.

## Features

- **Scraping**: Utilizes BeautifulSoup to scrape the latest article title, associated stock symbol, stock change percentage, and the time of post from SeekingAlpha's market news.
- **Discord Notification**: Posts the scraped information to a designated Discord channel in an embedded format.

- **Continuous Running**: Uses Flask to keep the script running, especially helpful for platforms like Replit.

## Requirements

- `requests`
- `discord.py`
- `BeautifulSoup4`
- `Flask`

## Setup

1. **Environment Variables**:

   - `DISCORD_TOKEN`: Your bot's token.
   - `CHANNEL_ID`: The ID of the channel where you want the bot to send messages.

2. **Permissions**:
   Ensure that the bot has permission to send messages to the desired channel.

3. **Dependencies**:
   Install all required modules using pip:

   ```
   pip install requests discord.py beautifulsoup4 Flask
   ```

## How it Works

1. The bot logs into Discord upon starting.

2. It then continuously checks SeekingAlpha's market news page every minute.

3. If there's a new article since the last check, the bot extracts the relevant data and posts it to the specified Discord channel.

4. A Flask app is initiated in a separate thread to ensure continuous running.

## Notes

- **Flask App**: The Flask app doesn't serve any routes; it's used to keep the script running on platforms that expect a bound port, like Replit.

- **Continuous Running**: If using Replit, make sure to have the 'Always On' feature enabled, especially if you want 24/7 uptime without manual intervention.

- **Web Scraping Caution**: Continuously scraping a website might lead to your IP getting blocked. Always ensure you're adhering to the website's `robots.txt` and terms of service.
