import discord
from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Extention_Loader: {self.__class__.__name__} has been loaded')
        
        #exeption handler send error message as embed
        @self.bot.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.CommandNotFound):
                return
            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(embed=discord.Embed(
                    title="Missing Required Argument",
                    description=f"{error}",
                    color=discord.Color.red()
                ))
            elif isinstance(error, commands.MissingPermissions):
                await ctx.send(embed=discord.Embed(
                    title="Missing Permissions",
                    description=f"{error}",
                    color=discord.Color.red()
                ))
            elif isinstance(error, commands.BotMissingPermissions):
                await ctx.send(embed=discord.Embed(
                    title="Bot Missing Permissions",
                    description=f"{error}",
                    color=discord.Color.red()
                ))
            elif isinstance(error, commands.CommandOnCooldown):
                await ctx.send(embed=discord.Embed(
                    title="Command On Cooldown",
                    description=f"{error}",
                    color=discord.Color.red()
                ))
            elif isinstance(error, commands.CheckFailure):
                await ctx.send(embed=discord.Embed(
                    title="Check Failure",
                    description=f"{error}",
                    color=discord.Color.red()
                ))
            elif isinstance(error, commands.CommandInvokeError):
                await ctx.send(embed=discord.Embed(
                    title="Command Invoke Error",
                    description=f"{error}",
                    color=discord.Color.red()
                ))
            elif isinstance(error, commands.CommandOnCooldown):
                await ctx.send(embed=discord.Embed(
                    title="Command On Cooldown",
                    description=f"{error}",
                    color=discord.Color.red()
                ))
            elif isinstance(error, commands.CommandNotFound):
                await ctx.send(embed=discord.Embed(
                    title="Command Not Found",
                    description=f"{error}",
                    color=discord.Color.red()
                ))
            elif isinstance(error, commands.CommandError):
                await ctx.send(embed=discord.Embed(
                    title="Command Error",
                    description=f"{error}",
                    color=discord.Color.red()
                ))
            else:
                await ctx.send(embed=discord.Embed(
                    title="Unknown Error",
                    description=f"{error}",
                    color=discord.Color.red()
                ))
                raise error

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
