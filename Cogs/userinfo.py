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
        embed = discord.Embed(title=user.name, description=f"{user.mention}'s info", color=embed_color_moderation)
        embed.add_field(name="User ID", value=user.id)
        embed.add_field(name="Account Created", value=user.created_at)
        embed.add_field(name="Joined Server", value=user.joined_at)
        embed.add_field(name="Status", value=user.status)
        embed.add_field(name="Nickname", value=user.nick)
        embed.add_field(name="Top Role", value=user.top_role)
        embed.add_field(name="Playing", value=user.activity)
        embed.add_field(name="Roles", value=user.roles)
        embed.add_field(name="Voice Channel", value=user.voice)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed, delete_after=10)


def setup(bot):
    bot.add_cog(userinfo(bot))