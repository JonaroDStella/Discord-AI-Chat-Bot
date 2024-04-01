import discord
from discord.ext import commands
import importlib
from config import *
from utils.Bots import CentralBot
from utils import AIFunction

class chat_cmds(commands.Cog):
    def __init__(self,  client: CentralBot):
        importlib.reload(AIFunction)
        self.client = client
        self.client.userdb.data.prompt = PROMPT
        self.client.userdb.data.limit = HISTORY_LIMIT
        self.client.userdb.data.voice_id = VOICE_ID
        self.client.userdb.data.history = []
        self.client.userdb.sync_all_data()

    @commands.command(name='history')
    async def history(self, ctx: commands.Context):
        chat = self.client.userdb.get_user(ctx.author.id)
        history = '\n'.join(map(str, chat.data.history))
        await ctx.channel.send(f"```{history if history != '' else 'None'}```")

    @commands.command(name='clear-history')
    async def clear_history(self, ctx: commands.Context):
        chat = self.client.userdb.get_user(ctx.author.id)
        chat.data.history.clear()
        await ctx.channel.send('```cleaned```')

    @commands.command(name= 'join')
    async def join(self, ctx: commands.Context):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if ctx.author.voice == None:
            await ctx.channel.send("You are not connected to any voice channel")
        elif voice == None:
            voiceChannel = ctx.author.voice.channel
            await voiceChannel.connect()
        else:
            await ctx.channel.send("Already connected to a voice channel")

    @commands.command(name= 'leave')
    async def leave(self, ctx: commands.Context):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice == None:
            await ctx.channel.send("The Bot is not connected to a voice channel")
        else:
            await voice.disconnect()

    @commands.Cog.listener()
    async def on_message(self, ctx: discord.Message):
        if ctx.author == self.client.user:
            return

        if ctx.content.startswith(CHAT_PREFIX):
            msg = ctx.content[len(CHAT_PREFIX):].strip()
            print(f'{ctx.channel.name} : ')
            print(f'{ctx.author} > {msg}')

            user = self.client.userdb.get_user(ctx.author.id)

            sta, reply = await self.client.loop.run_in_executor(None, AIFunction.make_completion, user, msg)
            if not sta:
                print(reply)
                await ctx.channel.send('Completion failed')
                return

            print(f'{self.client.user} : {reply}')
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

            if voice:
                async with ctx.channel.typing():
                    jp_reply = await self.client.loop.run_in_executor(None, AIFunction.translation, reply, 'japanese')
                    print('translated :', jp_reply)
                    print(user.data.voice_id)
                    await self.client.loop.run_in_executor(None, AIFunction.Voice, voice, user.data.voice_id, jp_reply)

            await ctx.channel.send(reply)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(chat_cmds(client))
