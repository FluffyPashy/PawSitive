import discord
from discord.ext import commands
from ruamel import yaml
from ruamel.yaml import YAML
from pathlib import Path
import os

yaml = YAML()

cwd = Path(__file__).parents[0]
cwd = str(cwd)

# Get config.yml
with open((cwd+'/settings/config.yml'), "r", encoding="utf-8") as file:
    config = yaml.load(file)

with open((cwd+'/settings/secrets.yml'), "r", encoding="utf-8") as file:
    secrets = yaml.load(file)

class Greetings(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self._last_member = None

# Defining some things
space = ("#" * 50) + "\n"
space2 = "\n"

# Intents
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(config['Prefix'], intents = intents)

# Load cogs
initial_extensions = [
    "Cogs.help",
    "Cogs.ping"
]
print(space + "Initializing Extension:")

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension}")

print(space + space2)

@bot.event
async def on_ready():
    print(f"Bot has logged in as: {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name = config['Prefix']))
    print("Discord version: " + discord.__version__)
    print(space2 + space + "\nBot_Logging: \n")

bot.run(secrets['Token'])