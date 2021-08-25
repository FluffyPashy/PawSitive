import discord
from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Extention_Loader: {self.__class__.__name__} has been loaded')
        # Work in progress
def setup(bot):
    bot.add_cog(ErrorHandler(bot))
