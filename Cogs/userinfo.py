import discord
from discord.ext import commands

from ruamel import yaml
from ruamel.yaml import YAML
from pathlib import Path

import datetime

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
        
        #create embed message with information from given userid
        embed = discord.Embed(title=f"{user}", description=f"{user.mention}", color= int(config['Embed Color']['Info'], 16))
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Nickname", value=user.nick, inline=True)
        embed.add_field(name="Status", value=user.raw_status, inline=True)
        embed.add_field(name="Roles", value=", ".join([role.mention for role in user.roles if role.name != "@everyone"]), inline=True)
        await ctx.send(embed=embed, delete_after=60)

class userinfo_mod(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #userinfo command user has role moderator or admin
    @commands.command(name= "userinfo_mod", aliases = ["uim"], hidden = True, pass_context = True)
    #has one of these roles: moderator, admin
    @commands.has_any_role(config['Roles']['Mod'], config['Roles']['Admin'])
    async def userinfo_mod(self, ctx, user: discord.Member):
        #delete command message
        await ctx.message.delete()

        #create embed message with information from given userid
        embed = discord.Embed(title=f"{user}", description=f"{user.mention}", color= int(config['Embed Color']['Info'], 16))
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="User ID", value=user.id, inline=True)
        embed.add_field(name="Nickname", value=user.nick, inline=True)
        embed.add_field(name="Status", value=f"{user.raw_status}\n{user.activity}", inline=True)

        #Calculate user creation and joinend date until now in days
        created_ago = f"{(datetime.datetime.now() - user.created_at).days}"
        joinend_ago = f"{(datetime.datetime.now() - user.joined_at).days}"


        # days = int(created_at_days_ago)
        # years = days / 365
        # rest_of_years = years % 1
        # years -= rest_of_years
        # month = rest_of_years * 30.417
        # rest_of_month = month % 1
        # month -= rest_of_month
        # days = int(rest_of_month * 30.417)
        # rest_of_days = days % 1
        # days -= rest_of_days
        
        #create function to convert days to years, months, days
        def days_convert(days):
            years = days // 365
            days = days % 365
            months = days // 30
            days = days % 30
            return (years, months, days)

        #embed message with joinend and created date in YYYY-MM-DD format
        embed.add_field(name="Created", value=f"{user.created_at.strftime('%d %b %Y')}\n **-** {days_convert(int(created_ago))[0]} years, {days_convert(int(created_ago))[1]} months, {days_convert(int(created_ago))[2]} days ago", inline=True)
        embed.add_field(name="Joinend", value=f"{user.joined_at.strftime('%d %b %Y')}\n **-** {days_convert(int(joinend_ago))[0]} years, {days_convert(int(joinend_ago))[1]} months, {days_convert(int(joinend_ago))[2]} days ago", inline=True)

        embed.add_field(name="Roles", value=", ".join([role.mention for role in user.roles if role.name != "@everyone"]), inline=True)
        await ctx.send(embed=embed, delete_after=60)


def setup(bot):
    bot.add_cog(userinfo(bot))
    bot.add_cog(userinfo_mod(bot))