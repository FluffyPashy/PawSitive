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

class userinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Event
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Extention_Loader: {self.__class__.__name__} has been loaded')

    #if command userinfo executed send embed message with information from given userid [WIP]
    @commands.command()
    async def userinfo(self, ctx, user: discord.Member):
        #delete command message
        await ctx.message.delete()

        #if user is not in server send embed message with error
        if user not in ctx.guild.members:
            embed = discord.Embed(title="Error", description="User not found in server", color= int(config['Embed Color']['Warning'], 16))
            await ctx.send(embed=embed)
        else:
            #create embed message with information from given userid
            embed = discord.Embed(title=f"{user}", description=f"{user.mention}", color= int(config['Embed Color']['Info'], 16))
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(name="User ID", value=user.id, inline=True)
            embed.add_field(name="Nickname", value=user.nick, inline=True)
            embed.add_field(name="Status", value=user.status, inline=True)
            embed.add_field(name="Joined Server", value=user.joined_at, inline=True)
            embed.add_field(name="Created Account", value=user.created_at, inline=True)
            embed.add_field(name="Roles", value=len(user.roles), inline=True)
            #send embed message
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(userinfo(bot))