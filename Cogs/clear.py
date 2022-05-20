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

class Clear(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Event
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Extention_Loader: {self.__class__.__name__} has been loaded')

    # Commands
    # clear + amount/dm
    @commands.command(pass_context = True)
    async def clear(self, ctx, args = None):

        def mess_is_not_pinned(mess):
            return not mess.pinned
    
        if args is None:
            await ctx.channel.purge(check = mess_is_not_pinned)
            
            clearmsg = discord.Embed(
                title = 'Moderation',
                description = f'All messages of #{ctx.channel} have been deleted by {ctx.author}',
                color = embed_color_moderation)
            
            await ctx.send(embed = clearmsg, delete_after = 10)

        elif args.isdigit():
            count = int(args) + 1
            deleted = await ctx.channel.purge(limit = count, check = mess_is_not_pinned)

            if args.isdigit() < 1:
                clearmsgdigit = discord.Embed(
                    title = 'Moderation',
                    description = '**{}** messages have been deleted in #'.format(len(deleted) - 1) + f'{ctx.channel} by {ctx.author}',
                    color = embed_color_moderation)
                await ctx.send(embed = clearmsgdigit, delete_after = 10)

            if args.isdigit() == 1:
                clearmsgdigit = discord.Embed(
                    title = 'Moderation',
                    description = '**{}** message has been deleted in #'.format(len(deleted) - 1) + f'{ctx.channel} by {ctx.author}',
                    color = embed_color_moderation)
                await ctx.send(embed = clearmsgdigit, delete_after = 10)
        else:
            await ctx.channel.purge(limit = 1)
            invalidarg = discord.Embed(
                title = 'Whoops',
                description = f'clear ~**{args}** is not a number!',
                color = embed_color_warning)
            await ctx.send(embed = invalidarg, delete_after = 10)

class DelDM(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Commands
    @commands.command()
    async def deldm(self, ctx):
        user = ctx.author

        await ctx.channel.purge(limit = 1)

        async for message in user.history(limit = 100):
            if message.author == self.bot.user:
                await message.delete()


def setup(bot):
    bot.add_cog(Clear(bot))
    bot.add_cog(DelDM(bot))
