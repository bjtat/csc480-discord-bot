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
            # await message.channel.send(f"Message is: {message.content}") # debug
            cleaned_msg = clean_msg(message.content)
            keyword_list = test_model(cleaned_msg)
            # await message.channel.send(f"Keywords is: {keyword_list}") # debug
            if keyword_list:
                if keyword_list[0] == "git":
                    git_word = get_correct_msg(keyword_list)
                    if git_word == None:
                        await message.channel.send("Sorry, I don't know that command yet.")
                    else:
                        filetext = read_git_file(git_word)
                        await message.channel.send(filetext)
                else:
                    clean_keyword_list = fuzzy_match(keyword_list)
                    # await message.channel.send(f"Clean keywords is: {clean_keyword_list}") # debug
                    (similar_word, confidence_level) = git_similarity(clean_keyword_list)
                    # await message.channel.send(f"Confidence level is: {confidence_level}") # debug
                    if confidence_level > 0.8:
                        await message.channel.send(f"Most similar git command is: {similar_word}\n\n")
                        git_file = read_git_file(similar_word)
                        await message.channel.send(git_file)
                    else:
                        await message.channel.send("Sorry, I'm not sure I understand. Please try again.")
            else:
                await message.channel.send("Sorry, I'm not sure I understand. Please try again.")

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
