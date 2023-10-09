from time import time

import discord
from discord.ext import commands

from utils import chatting
from utils.VoiceVox import Voicevox
from config import FFMPEG_PATH


class Chat_Bot:
    def __init__(self, prefix: str, token: str, prompt: str, voice_id, limit: int, admin_id: str) -> None:
        self.prefix = prefix
        self.token = token
        self.prompt = prompt
        self.limit = limit
        self.voice_id = voice_id
        self.total_token = 0
        self.admin_id = admin_id
        self.DB = chatting.UserDatabase(
                    prompt=self.prompt,
                    limit=self.limit
                )
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.bot = commands.Bot(
            command_prefix=self.prefix,
            intents=self.intents)

    def main(self) -> None:
        
        bot = self.bot
        @bot.event
        async def on_ready():
            print('Bot ready as', bot.user)

        @bot.listen()
        async def on_message(ctx):
            if ctx.author == bot.user :
                return
            
            if ctx.content[:2] == '> ':
                msg = ctx.content[2:].strip()
                print(f'{ctx.channel.name} : ')
                print(f'{ctx.author} > {msg}')

                chat = self.DB.get_user(ctx.author.id, prompt=self.prompt, limit=self.limit).chat

                if chat.starttime - time() > 600:
                    chat.history = []

                if not chat.make_completion(msg):
                    await ctx.channel.send('Completion failed')
                    return
                print(f'{bot.user} : {chat.reply}')
                print(f'{chat.token}')
                
                voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

                if voice:
                    async with ctx.channel.typing():
                        jp = chatting.Chat(history=[], prompt='translate to japanese', limit=10, token=0)
                        jp.make_completion(chat.reply)
                        print('translated :', jp.reply)
                        self.total_token += jp.lasttoken
                        self.Voice(ctx=ctx, jp=jp.reply)
                await ctx.channel.send(chat.reply)
                self.total_token += chat.lasttoken
                return

        @bot.remove_command('help')
        @bot.command(name='help')
        async def help(ctx):
            await ctx.channel.send('''
To execute a command : 
```$ (command)```
To chat with bot : 
```> (message)```
command :
```
    ping
    whoami
    total-cost
    previous-cost
    history
    clear-history
    set [NAME] [VALUE]
    show [NAME...]
```
voice :
```
    join
    leave
```
''')

        @bot.command(name='ping')
        async def ping(ctx):
            await ctx.channel.send('```Latency is {:.2f}ms```'.format(bot.latency*1000))
            
        @bot.command(name='whoami')
        async def whoami(ctx):
            await ctx.channel.send('```{} ({})```'.format(ctx.author, ctx.author.id))

        @bot.command(name='join')
        async def join(ctx):
            voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            if ctx.author.voice == None:
                await ctx.channel.send("You are not connected to any voice channel")
            elif voice == None:
                voiceChannel = ctx.author.voice.channel
                await voiceChannel.connect()
            else:
                await ctx.channel.send("Already connected to a voice channel")

        @bot.command(name='leave')
        async def leave(ctx):
            voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            if voice == None:
                await ctx.channel.send("The Bot is not connected to a voice channel")
            else:
                await voice.disconnect()

        @bot.command(name='show')
        async def show(ctx, *args):
            try:
                user = self.DB.get_user(ctx.author.id)
                values = map((lambda name, value: f'{name} :\n```{value}```'), args, map(
                    user.get_data, args))
                await ctx.channel.send('\n'.join(values))
            except:
                await ctx.channel.send('Unknown variable name')

        @bot.command(name='total-cost')
        async def total_cost(ctx):
            await ctx.channel.send(
                'Spent {} tokens in total,\nequals {:.4f}USD'.format(self.total_token, self.total_token*0.0000015))

        @bot.command(name='set')
        async def set(ctx, *args):
            try:
                user = self.DB.get_user(ctx.author.id)
                user.data[args[0]] = ' '.join(args[1:])
                await ctx.channel.send('{} now is {}'.format(args[0],user.get_data(args[0])))
            except:
                await ctx.channel.send('Incompleted information')

        @bot.command(name='setuser')
        async def setuser(ctx, *args):
            if ctx.author.id != self.admin_id:
                await ctx.channel.send('Permission denied')
                return
            if len(args) < 3:
                await ctx.channel.send('Incompleted information')
                return
            user = self.DB.get_user(args[0])
            user.data[args[1]] = ' '.join(args[2:])
            await ctx.channel.send('{} now is {}'.format(args[1],user.get_data(args[1])))

        @bot.command(name='previous-cost')
        async def previous_cost(ctx):
            chat = self.DB.get_user(ctx.author.id).chat
            await ctx.channel.send(
                'That was {} tokens,\nequals {:.4f}USD'.format(chat.lasttoken,
                                                                          chat.lasttoken*0.0000015))

        @bot.command(name='history')
        async def history(ctx):
            chat = self.DB.get_user(ctx.author.id).chat
            history = '\n'.join(map(str, chat.history))
            await ctx.channel.send('```' + (history if history != '' else 'None') + '```')

        @bot.command(name='clear-history')
        async def clear_history(ctx):
            chat = self.DB.get_user(ctx.author.id).chat
            chat.history.clear()
            await ctx.channel.send('```cleaned```')

        @bot.command(name='shutdown')
        async def shutdown(ctx):
            if ctx.author.id != self.admin_id:
                await ctx.channel.send('Permission denied')
                return
            await ctx.channel.send('bye')
            exit()

        bot.run(self.token)

    def Voice(self, ctx: discord.Message, jp: str):
        
            VOICE = Voicevox()
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            stream = VOICE.speak(jp, self.voice_id)
            if voice.is_playing():
                voice.stop()
            voice.play(discord.FFmpegPCMAudio(
                    source=stream, executable=FFMPEG_PATH),
                    after=lambda x: print('finished audio')
                    )