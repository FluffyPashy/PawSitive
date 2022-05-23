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
                color = int(config['Embed Color']['Moderation'], 16))
            
            await ctx.send(embed = clearmsg, delete_after = 10)

        elif args.isdigit():
            count = int(args) + 1
            deleted = await ctx.channel.purge(limit = count, check = mess_is_not_pinned)

            if args.isdigit() < 1:
                clearmsgdigit = discord.Embed(
                    title = 'Moderation',
                    description = '**{}** messages have been deleted in #'.format(len(deleted) - 1) + f'{ctx.channel} by {ctx.author}',
                    color = int(config['Embed Color']['Moderation'], 16))
                await ctx.send(embed = clearmsgdigit, delete_after = 10)

            if args.isdigit() == 1:
                clearmsgdigit = discord.Embed(
                    title = 'Moderation',
                    description = '**{}** message has been deleted in #'.format(len(deleted) - 1) + f'{ctx.channel} by {ctx.author}',
                    color = int(config['Embed Color']['Moderation'], 16))
                await ctx.send(embed = clearmsgdigit, delete_after = 10)
        else:
            await ctx.channel.purge(limit = 1)
            invalidarg = discord.Embed(
                title = 'Whoops',
                description = f'clear ~**{args}** is not a number!',
                color = int(config['Embed Color']['Critical'], 16))
            await ctx.send(embed = invalidarg, delete_after = 10)
            
def setup(bot):
    bot.add_cog(Clear(bot))
