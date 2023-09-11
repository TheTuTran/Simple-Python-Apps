import requests
import discord
import os
from discord.ext import tasks, commands
from bs4 import BeautifulSoup
import threading
from flask import Flask
import re
from collections import deque

TOKEN = os.environ['DISCORD_TOKEN']
CHANNEL_ID = int(os.environ['CHANNEL_ID'])

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

prev_article = ""


@bot.event
async def on_ready():
  print(f'Logged in as {bot.user.name}')
  check_news.start()


@tasks.loop(minutes=5)
async def check_news():
  global prev_article
  print("Checking news...")

  response = requests.get("https://seekingalpha.com/market-news")
  html = response.text
  soup = BeautifulSoup(html, 'html.parser')
  post_list_item = soup.find('article',
                             attrs={'data-test-id': 'post-list-item'})

  if post_list_item:
    # Grab title and url of article
    post_list_item_title = post_list_item.find(
        'a', attrs={'data-test-id': 'post-list-item-title'})
    output_title = post_list_item_title.text
    output_url = f"https://seekingalpha.com{post_list_item_title['href']}"

    if prev_article != output_title:
      prev_article = output_title
      # Footer content: symbol, symbol change, & date
      post_footer = post_list_item.find('footer',
                                        attrs={'data-test-id': 'post-footer'})
      output_symbol = None
      output_symbol_change = None

      footer_a = post_footer.find('a')
      if footer_a:
        symbol_span = footer_a.find_all('span')
        if symbol_span:

          if symbol_span and len(symbol_span) >= 2:
            output_symbol = symbol_span[0].text
            output_symbol_change = symbol_span[1].text
      output_time = post_footer.find('span',
                                     attrs={
                                         'data-test-id': 'post-list-date'
                                     }).text
      print("title =", output_title)
      print("Stock =", output_symbol)
      print("Stock Change =", output_symbol_change)
      print("Time =", output_time)
      print('-' * 50)

      # Create an embed for Discord
      embed = discord.Embed(
          title=output_title,
          url=output_url if output_url else "",
          description=
          f"Symbol: {output_symbol}\nStock Change: {output_symbol_change}",
          color=0x2ecc71 if output_symbol_change
          and "+" in output_symbol_change else 0xe74c3c)
      embed.add_field(name="Date", value=output_time, inline=False)
      channel = bot.get_channel(CHANNEL_ID)
      await channel.send(embed=embed)
    else:
      print("Same article still on top")
  else:
    print("Could not find post list item")


bot.run(TOKEN)


def run_flask():
  app = Flask(__name__)
  app.run(host='0.0.0.0', port=8080, use_reloader=False)


t = threading.Thread(target=run_flask)
t.start()
