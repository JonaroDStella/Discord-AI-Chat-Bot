from discord.ext import commands
import importlib
from utils.Bots import CentralBot
from utils import UserDB


class userdb_cmds(commands.Cog):
    def __init__(self,  client: CentralBot):
        importlib.reload(UserDB)
        self.client = client
        if 'userdb' not in self.client.__dict__:
            self.client.userdb = UserDB.UserDB()

    @commands.command(name='show')
    async def show(self, ctx: commands.Context, *args):
        user = self.client.userdb.get_user(ctx.author.id)
        output = ''
        if len(args) == 0:
            args = user.data.keys()
        for name in args:
            output += f'\n{name}: {user.data[name]}'
        await ctx.channel.send(f'```{output}```')

    @commands.command(name='set')
    async def set(self, ctx: commands.Context, *args):
        user = self.client.userdb.get_user(ctx.author.id)
        response = user.set_data(args[0], ' '.join(args[1:]))
        await ctx.channel.send(response)

    @commands.command(name='reset')
    async def reset(self, ctx: commands.Context):
        user = self.client.userdb.get_user(ctx.author.id)
        user.data = self.client.userdb.data.copy()
        await ctx.channel.send('```Reset and synced```')


async def setup(client: commands.Bot) -> None:
    await client.add_cog(userdb_cmds(client))
