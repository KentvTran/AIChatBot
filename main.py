import random
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv


# Replace 'YOUR_TOKEN_HERE' with the actual token you copied from the Discord Developer Portal
load_dotenv()
TOKEN = os.environ.get("DISCORD_TOKEN")

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

# help command
@client.command(name='help')
async def help_command(ctx):
    # Customize the help message as needed
    help_message = "Hi! This is EddyBot. Here are the available commands:\n" \
                   "!hello - Greet the bot\n" \
                   "!help - Display this help message"

    # Send help message to channel where command was invoked
    await ctx.send(help_message)


# Start the bot
client.run(TOKEN)
