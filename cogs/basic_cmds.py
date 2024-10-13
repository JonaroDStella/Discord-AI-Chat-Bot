from discord.ext import commands
from config import *
class basic_cmds(commands.Cog):
    def __init__(self,  client):
        self.client = client
    @commands.command(name='ping')
    async def ping(self, ctx: commands.Context):
        await ctx.channel.send('```Latency is {:.2f}ms```'.format(self.client.latency*1000))
    @commands.command(name='whoami')
    async def whoami(self, ctx: commands.Context):
        await ctx.channel.send(f'```{ctx.author} ({ctx.author.id})```')
async def setup(client: commands.Bot) -> None:
    await client.add_cog(basic_cmds(client))