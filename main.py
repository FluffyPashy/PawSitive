import discord
from discord.ext import commands, tasks

from ruamel import yaml
from ruamel.yaml import YAML
from pathlib import Path

from itertools import cycle
import datetime

########################################################################
# Define some things
########################################################################

# Folder struc and pathsystem
yaml = YAML()

cwd = Path(__file__).parents[0]
cwd = str(cwd)

# Loads in settings/config.yml
with open((cwd+'/settings/config.yml'), "r", encoding="utf-8") as file:
    config = yaml.load(file)

# Loads in settings/secrets.yml
with open((cwd+'/settings/secrets.yml'), "r", encoding="utf-8") as file:
    secrets = yaml.load(file)

# Debugging and cleaner console log
console_seperator = "\n" + ("#" * 50) + "\n"

# Status cycle function
presence = cycle([config['Presence']['Display1'], config['Presence']['Display2'], config['Prefix'] + config['Presence']['Display3'],])

# Log Channel
log_channel_id = config['Log Channel ID']

# Embed color types
embed_info = discord.Color.from_rgb(
    config['Embed Settings']['Color']['Info']['r'],
    config['Embed Settings']['Color']['Info']['g'],
    config['Embed Settings']['Color']['Info']['b']
)
embed_update = discord.Color.from_rgb(
    config['Embed Settings']['Color']['Update']['r'],
    config['Embed Settings']['Color']['Update']['g'],
    config['Embed Settings']['Color']['Update']['b']
)
embed_announcement = discord.Color.from_rgb(
    config['Embed Settings']['Color']['Announcement']['r'],
    config['Embed Settings']['Color']['Announcement']['g'],
    config['Embed Settings']['Color']['Announcement']['b']
)
embed_warning = discord.Color.from_rgb(
    config['Embed Settings']['Color']['Warning']['r'],
    config['Embed Settings']['Color']['Warning']['g'],
    config['Embed Settings']['Color']['Warning']['b']
)

class Greetings(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self._last_member = None

# Intents
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(config['Prefix'], intents = intents)

# Load cogs
initial_extensions = sorted([
    "Cogs.help",
    "Cogs.ping"
])

print(f"{console_seperator}\nInitializing Cogs:")

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension}")

print(f"{console_seperator}\n")

@bot.event
async def on_ready():
    # Basic console log
    print(f"Bot has logged in as {bot.user} and connected to {bot.user.id}")
    print("Discord version: " + discord.__version__)
    print(f"\n{bot.user.name} is ready to operate")
    print(f"{console_seperator}Bot_Logging: \n")

    # Bot start embed message
    bot_start = discord.Embed(
        title = f"{bot.user.name} is now Online!",
        color = embed_info,
        timestamp = datetime.datetime.now(datetime.timezone.utc)
    )
    # additional footer
    bot_start.set_footer(
        text = "Systemconsole",
        icon_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Infobox_info_icon.svg/160px-Infobox_info_icon.svg.png"
    )
    
    # Send embed message into log_channel
    log_channel = bot.get_channel(log_channel_id)
    await log_channel.send(embed = bot_start)

    # Start task loop changePresence
    change_presence.start()

# Status cycle loop
@tasks.loop(seconds=10)
async def change_presence():
    await bot.change_presence(activity=discord.Game(next(presence)), status=discord.Status.online)

# Restart command
@bot.command(name = "restart", aliases = ["rs"], help = "Restarts PawSitive(Bot)")
@commands.has_role(config['Roles']['Dev'])
async def restart(ctx):
    bot_restart = discord.Embed(
        title = f"{bot.user.name} is restarting!",
        color = embed_warning,
        timestamp = datetime.datetime.now(datetime.timezone.utc)
    )
    bot_restart.set_author(
        name = ctx.author.name,
        icon_url = ctx.author.avatar_url
    )
    # additional footer
    bot_restart.set_footer(
        text = "Systemconsole",
        icon_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Infobox_info_icon.svg/160px-Infobox_info_icon.svg.png"
    )
    log_channel = bot.get_channel(log_channel_id)
    await log_channel.send(embed = bot_restart)
    await bot.close()

# Run bot cmd
bot.run(secrets['Token'], bot=True, reconnect=True)