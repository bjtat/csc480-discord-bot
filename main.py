import discord
import os
import spacy
from dotenv import load_dotenv
from Scripts import nlp_model
from collections import Counter
from string import punctuation

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

    if message.content.startswith('$robin'):
        await message.channel.send(f"message is: [{message.content}]")
        await message.channel.send(f"keywords is: [{test_model(message.content)}]")

def test_model(msg):
    keywords = nlp_model.get_keywords(model, msg)
    sorted_keywords = [x[0] for x in Counter(keywords).most_common(min(MIN_KEYWORDS, len(keywords)))]
    return (' '.join(sorted_keywords))

if __name__ == '__main__':
    load_dotenv()
    print(f"token is: {os.getenv('TOKEN')}")
    client.run(os.getenv('TOKEN'))