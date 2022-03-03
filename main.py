import discord
import os
import spacy
from dotenv import load_dotenv
from collections import Counter
from string import punctuation

from Scripts import nlp_model

client = discord.Client()
model = spacy.load('en_core_web_md')

MIN_KEYWORDS = 10

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('hello!')

    if message.content.startswith('Robin,'):
        await message.channel.send(f"message is: [{message.content}]")
        cleaned_msg = clean_msg(message.content)
        keyword_list = test_model(cleaned_msg)
        await message.channel.send(f"keywords is: [{keyword_list}]")
        formatted = format_keywords(keyword_list)
        await message.channel.send(formatted)

def clean_msg(msg):
    cm = msg.removeprefix("Robin,")
    cm = cm.strip()
    return cm

def format_keywords(keywords):
    formatted = ""
    for count, keyword in enumerate(keywords):
        formatted = formatted + f"{count}. {keyword}\n"
    return formatted

def test_model(msg):
    keywords = nlp_model.get_keywords(model, msg)
    sorted_keywords = [x[0] for x in Counter(keywords).most_common(min(MIN_KEYWORDS, len(keywords)))]
    return (' '.join(sorted_keywords))

if __name__ == '__main__':
    load_dotenv()
    print(f"token is: {os.getenv('TOKEN')}")
    client.run(os.getenv('TOKEN'))
