import discord
import os
import spacy
from dotenv import load_dotenv
from collections import Counter
from string import punctuation

from Scripts import nlp_model
from Scripts.similarity_model import git_similarity
from Scripts.fuzzy_model import fuzzy_match

client = discord.Client()
model = spacy.load('en_core_web_md')

MIN_KEYWORDS = 10

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    # ignore the message if it comes from the bot itself
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('hello!')

    if message.content.startswith('Robin,'):
        async with message.channel.typing():
            await message.channel.send(f"message is: {message.content}")
            cleaned_msg = clean_msg(message.content)
            keyword_list = test_model(cleaned_msg)
            await message.channel.send(f"keywords is: {keyword_list}")
            # formatted = format_keywords(keyword_list)
            # await message.channel.send(keyword_list)
            clean_keyword_list = fuzzy_match(keyword_list)
            await message.channel.send(f"clean keywords is: {clean_keyword_list}")
            similar_word = git_similarity(clean_keyword_list)
            await message.channel.send(f"most similar git command is: {similar_word}")
            git_file = read_git_file(similar_word)
            await message.channel.send(git_file)
            if "git" in keyword_list:
                filetext = "some error has occurred"
                git_word = get_correct_msg(keyword_list)
                filetext = read_git_file(git_word)
                await message.channel.send(filetext)

def get_correct_msg(keywords):
    git_words = ["add", "branch", "checkout", "clone", "commit", "config", "init", "pull", "push", "status"]
    for word in keywords:
        if word in git_words:
            return word

def read_git_file(command):
    filepath = f"./git_entries/{command}.txt"
    with open(filepath, 'r') as f:
        return f.read()

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
    return sorted_keywords

if __name__ == '__main__':
    load_dotenv()
    print(f"token is: {os.getenv('TOKEN')}")
    client.run(os.getenv('TOKEN'))
