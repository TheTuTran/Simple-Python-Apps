import requests
import discord
import os
from discord.ext import tasks, commands
from bs4 import BeautifulSoup
import re
from collections import deque
from keep_alive import keep_alive
import datetime

keep_alive()

TOKEN = os.environ['DISCORD_TOKEN']
CHANNEL_ID = int(os.environ['CHANNEL_ID'])

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

prev_articles = deque(maxlen=5)


def convert_time_to_proper_format(time_str):
  if 'Today' in time_str:
    today_date = datetime.datetime.now().strftime('%m-%d-%Y')
    time_only = time_str.split(",")[-1].strip()
    return today_date + " " + time_only
  elif 'Now' in time_str:
    return datetime.datetime.now().strftime('%m-%d-%Y %I:%M %p')
  else:
    return time_str


@bot.event
async def on_ready():
  print(f'Logged in as {bot.user.name}')
  check_news.start()


@tasks.loop(minutes=3)
async def check_news():
  global prev_article
  print("Checking news...")

  response = requests.get("https://seekingalpha.com/market-news")
  html = response.text
  soup = BeautifulSoup(html, 'html.parser')
  post_list_items = soup.find_all('article',
                                  attrs={'data-test-id': 'post-list-item'},
                                  limit=3)

  for post_list_item in post_list_items:
    # Grab title and url of article
    post_list_item_title = post_list_item.find(
        'a', attrs={'data-test-id': 'post-list-item-title'})
    output_title = post_list_item_title.text

    # check to see if its in the list of previous articles
    if output_title not in prev_articles:
      prev_articles.append(output_title)

      # Article url and image url
      output_url = f"https://seekingalpha.com{post_list_item_title['href']}"
      output_img_url = ""
      img_tag = post_list_item.find('img')
      if img_tag and 'src' in img_tag.attrs:
        if "https" not in img_tag['src']:
          output_img_url = f"https://seekingalpha.com/{img_tag['src']}"
        else:
          output_img_url = f"{img_tag['src']}"

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
            output_time = convert_time_to_proper_format(output_time)
      print("title =", output_title)
      print("Stock =", output_symbol)
      print("Stock Change =", output_symbol_change)
      print("Time =", output_time)
      print("Image Url =", output_img_url)
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
          # Set image to the embed if we found one
      if img_tag and 'src' in img_tag.attrs:
        embed.set_image(url=output_img_url)
      await channel.send(embed=embed)

    else:
      print("Same article still on top")
  else:
    print("Could not find post list item")


bot.run(TOKEN)
