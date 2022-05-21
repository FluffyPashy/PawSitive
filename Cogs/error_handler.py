import discord
from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Extention_Loader: {self.__class__.__name__} has been loaded')
        
        #exeption handler
        @self.bot.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.CommandNotFound):
                await ctx.send(f'Command not found!')
            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(f'Missing required argument!')
            elif isinstance(error, commands.MissingPermissions):
                await ctx.send(f'You do not have the required permissions!')
            elif isinstance(error, commands.CommandOnCooldown):
                await ctx.send(f'You are on cooldown!')
            else:
                await ctx.send(f'An error occured!')
                raise error
        
def setup(bot):
    bot.add_cog(ErrorHandler(bot))
