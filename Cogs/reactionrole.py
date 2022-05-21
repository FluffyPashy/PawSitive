import discord
from discord.ext import commands

from ruamel import yaml
from ruamel.yaml import YAML
from pathlib import Path

########################################################################
# Define some things
########################################################################

# Folder struc and pathsystem
yaml = YAML()

cwd = Path(__file__).parents[1]
cwd = str(cwd)

# Loads in settings/config.yml
with open((cwd+'/settings/config.yml'), "r", encoding="utf-8") as file:
    config = yaml.load(file)

embed_color_moderation = discord.Color.from_rgb(0, 0, 255)
embed_color_warning = discord.Color.from_rgb(252, 0, 0)

class reactionrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Event
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Extention_Loader: {self.__class__.__name__} has been loaded')

    #give user the verified role after reacting to rules & regulations
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if payload.message_id == config['Reaction Roles']['Verify']['Message ID']:
            if payload.emoji.name == config['Reaction Roles']['Verify']['Emoji']:
                role = discord.utils.get(guild.roles, name=config['Reaction Roles']['Verify']['Verify Role'])
                if role in member.roles:
                    pass
                else:
                    await member.add_roles(role)
                    print(f'{member} has been given the role {role}')
                    await member.send(f'You are now verified!')
                    await member.send(config['Reaction Roles']['Verify']['Verify Message'])
            else:
                pass
    

def setup(bot):
    bot.add_cog(reactionrole(bot))