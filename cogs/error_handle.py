import discord
from discord.ext import commands
from utils.Bots import CentralBot


class error_handle(commands.Cog):
    def __init__(self,  client: CentralBot):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: discord.DiscordException):
        if isinstance(error, commands.CommandNotFound):
            await ctx.channel.send(error.args[0])
        elif isinstance(error, commands.MissingPermissions):
            await ctx.channel.send('Permission denied')
        elif isinstance(error, AttributeError):
            await ctx.channel.send(error[0])
        else:
            print(error)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(error_handle(client))
