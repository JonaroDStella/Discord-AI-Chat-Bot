from discord.ext import commands
import importlib
from config import *
from utils.Bots import CentralBot


class admin_cmds(commands.Cog):
    def __init__(self,  client: CentralBot):
        self.client = client

    @commands.command(name='user-list')
    @commands.has_permissions(administrator=True)
    async def user_list(self, ctx: commands.Context):
        users = [await self.client.fetch_user(id) for id in self.client.userdb.users.keys()]
        res = '\n'.join(map(lambda x: f'{x.name} : {x.id}', users))
        await ctx.channel.send(f'```{res}```')

    @commands.command(name='setuser')
    @commands.has_permissions(administrator=True)
    async def setuser(self, ctx: commands.Context, *args):
        if len(args) < 3:
            await ctx.channel.send('Incompleted information')
            return
        try:
            user_id = int(args[0])
        except:
            await ctx.channel.send('User ID should be integer')
            return
        user = self.client.userdb.get_user(user_id)
        response = user.set_data(args[1], ' '.join(args[2:]))
        await ctx.channel.send(response)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(admin_cmds(client))
