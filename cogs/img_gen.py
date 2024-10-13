import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from config import *
from utils.Bots import CentralBot
from utils import AIFunction
import importlib


class img_gen(commands.Cog):
    def __init__(self,  client: CentralBot):
        importlib.reload(AIFunction)
        self.client = client

    @app_commands.command(name = "generate_image", description = "Generates an image from given prompt")
    @app_commands.describe(model = "Model", size = "Choose resolution", prompt='Descibe the image')
    @app_commands.choices(
        model = [
            Choice(name = "DALL·E 3", value = "dall-e-3"),
            Choice(name = "DALL·E 2", value = "dall-e-2")
        ],
        size = [
            Choice(name = "1024x1024", value = "1024x1024"),
            Choice(name = "1024x1792", value = "1024x1792"),
            Choice(name = "1792x1024", value = "1792x1024")
        ],
    )
    async def generate_image(self, interaction: discord.Interaction, model: Choice[str], size: Choice[str], prompt: str):
        await interaction.response.send_message('wait a second uwu...')
        url = await AIFunction.generate_image(
                model=model.value,
                prompt=prompt,
                size=size.value)
        await interaction.edit_original_response(content=url)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(img_gen(client))
