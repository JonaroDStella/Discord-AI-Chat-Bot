from discord.ext import commands
import importlib
import config
from pyngrok import ngrok, conf

importlib.reload(config)
conf.get_default().auth_token = config.NGROK_KEY

class ngrok_cmds(commands.Cog):
    def __init__(self,  client):
        self.client = client
    @commands.command(name='ngrok-ssh')
    async def ngrok_ssh(self, ctx: commands.Context):
        for tunnel in ngrok.get_tunnels():
            if tunnel.proto == "tcp":
                await ctx.channel.send(f'```Already connected at: {tunnel.public_url}```')
                return
        try:
            url = ngrok.connect("22", "tcp").public_url
            await ctx.channel.send(f'```Connected at: {url}```')
        except Exception as e:
            await ctx.channel.send(f'```{e.args[0]}```')

    @commands.command(name='ngrok-tunnels')
    async def ngrok_tunnels(self, ctx: commands.Context):
        tunnels = ngrok.get_tunnels()
        if len(tunnels) == 0:
            await ctx.channel.send(f'```No tunnel created!```') 
            return   
        await ctx.channel.send(f'```{"\n".join(map(str, ))}```')
    
    @commands.command(name='ngrok-kill')
    async def ngrok_kill(self, ctx: commands.Context, *args):
        if len(args) == 0:
            await ctx.channel.send(f'```args pls```')
            return
        ngrok.disconnect(args[0])
        await ctx.channel.send(f'```{args[0]} Executed```')

    @commands.command(name='ngrok-kill-all')
    async def ngrok_kill_all(self, ctx: commands.Context):
        for tunnel in ngrok.get_tunnels():
            ngrok.disconnect(tunnel.public_url)
        await ctx.channel.send(f'```Killed```')
        
async def setup(client: commands.Bot) -> None:
    await client.add_cog(ngrok_cmds(client))