import random
import discord
import requests
import json
import os
from discord.ext import commands
from dotenv import load_dotenv

# Replace 'YOUR_TOKEN_HERE' with the actual token you copied from the Discord Developer Portal
load_dotenv()
TOKEN = os.environ.get("DISCORD_TOKEN")
JOKEAPI = os.environ.get("JOKEAPI")

# This enables features for bot, rn message
intents = discord.Intents.default()
intents.message_content = True

# Create an instance of the bot with intents
# Prefix calls bot like {!help}
client = commands.Bot(command_prefix='!', intents=intents)

# client.event are for bot features
# Event handler for when the bot is ready
# On ready = receive commands
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    print("------------------------------------")

# event when members join
@client.event
async def on_member_join(member):
    channel = client.get_channel(1206700172520853528)
    await channel.send(f"Greetings {member.mention}! Welcome to the server.")

# event when members leave
@client.event
async def on_member_remove(member):
    channel = client.get_channel(1206700172520853528)
    await channel.send(f"Have a good day {member.mention}!")

# Joke command
@client.command(name='joke')
async def joke(ctx):
    await ctx.send(f"Here's a joke for you:\n")

    url = "https://jokeapi-v2.p.rapidapi.com/joke/Any"

    headers = {
        "X-RapidAPI-Key": JOKEAPI,
        "X-RapidAPI-Host": "jokeapi-v2.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers)
        joke_data = response.json()

        # Print the entire JSON response
        print(joke_data)

        # Check the type of the joke
        joke_type = joke_data.get('type', 'single')

        if joke_type == 'twopart':
            setup = joke_data.get('setup', 'No setup found')
            delivery = joke_data.get('delivery', 'No delivery found')
            await ctx.send(f"**Setup:** {setup}\n**Delivery:** {delivery}")
        elif joke_type == 'single':
            joke = joke_data.get('joke', 'No joke found')
            await ctx.send(f"**Joke:** {joke}")
        else:
            await ctx.send("Unknown joke type")

    except Exception as e:
        # Handle errors
        await ctx.send(f"Error getting a joke: {e}")

# Goodbye command
@client.command()
async def goodbye(ctx):
    await ctx.send("Goodbye, hope you have a good rest of your day!")

# Event handler for when a message is received
@client.event
async def on_message(message):
    # Ignore messages from the bot itself to prevent infinite loops
    if message.author == client.user:
        return

    # Respond to a specific command
    if message.content.lower().startswith('!hello'):
        # List of possible responses
        responses = ['Wassup my g!', 'Hello there!', 'Howdy!', 'Hey!']

        # Select a random response from the list
        response = random.choice(responses)

        # Send the random response
        await message.channel.send(response)

    # Process commands
    await client.process_commands(message)

# Start the bot
client.run(TOKEN)
