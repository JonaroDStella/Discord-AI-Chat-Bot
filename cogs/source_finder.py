import discord
from discord import app_commands
from discord.ext import commands
from config import *
import importlib
from utils.Bots import CentralBot
from utils import AIFunction
from urllib.parse import urlparse


class Select(discord.ui.Select):
    def __init__(self, url_dict: dict[str, str]):
        self.url_dict = url_dict
        options=[
            discord.SelectOption(label=name) for name in url_dict.keys()
            ]
        super().__init__(placeholder="Select an website",max_values=1,min_values=1,options=options)
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content=self.url_dict[self.values[0]], view=None)

class SelectView(discord.ui.View):
    def __init__(self, *, timeout = 180, url_dict: dict[str, str]):
        super().__init__(timeout=timeout)
        self.add_item(Select(url_dict=url_dict))

class source_cmds(commands.Cog):
    def __init__(self,  client: CentralBot):
        importlib.reload(AIFunction)
        self.client = client

    @commands.command(name='sauce')
    async def sauce(self, ctx: commands.Context):
        if not ctx.message.reference:
            return await ctx.reply('pls reply to an attachment.')
        if not ctx.message.reference.resolved.attachments:
            return await ctx.reply('no attachments found.')
        for image in ctx.message.reference.resolved.attachments:
            ret, urls = await AIFunction.find_source(image)
            if ret :
                url_dict = {}
                for url in urls:
                    url_dict[urlparse(url).netloc] = url
                await ctx.channel.send(content="Select a website", view=SelectView(url_dict=url_dict))
            else:
                await ctx.channel.send(content=urls)

    @app_commands.command(name='source', description='Source finder')
    async def source(self, interaction: discord.Interaction, image: discord.Attachment):
        # await interaction.response.send_message('wait a second uwu...')
        ret, urls = await AIFunction.find_source(image)
        if ret :
            url_dict = {}
            for url in urls:
                url_dict[urlparse(url).netloc] = url
            await interaction.response.send_message(content="Select a website", view=SelectView(url_dict=url_dict))
        else:
            await interaction.response.send_message(content=urls)
    
async def setup(client: commands.Bot) -> None:
    await client.add_cog(source_cmds(client))
