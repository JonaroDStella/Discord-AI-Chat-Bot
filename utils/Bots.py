import discord
from discord.ext import commands
import os


class CentralBot(commands.Bot):
    def __init__(self, command_prefix: str, cogs_dir: str) -> None:
        self.coglist = []
        self.cogs_dir = cogs_dir
<<<<<<< HEAD
        if not self.cogs_dir.endswith('\\'):
            self.cogs_dir += '\\'
=======
        if not self.cogs_dir.endswith(os.sep):
            self.cogs_dir += os.sep
>>>>>>> 89908d9 (fixed to adapt new openai api)
        self.cogs_base = self.cogs_dir.replace(os.sep, '.')
        intents = discord.Intents.all()
        super().__init__(command_prefix=command_prefix, intents=intents)

        @self.command(name='reload-all-cogs', description='Reload all loaded cogs')
        @commands.has_permissions(administrator=True)
        async def reload_all_cogs(ctx: commands.Context) -> None:
            for ext in self.coglist:
                await self.reload_extension(ext)
            await ctx.channel.send('Reloaded')

        @self.command(name='reload-cogs', description='Reload cogs')
        @commands.has_permissions(administrator=True)
        async def reload_cogs(ctx: commands.Context, *args) -> None:
            for ext in args:
                try:
                    await self.reload_extension(self.cogs_base + ext)
                    await ctx.channel.send(f'Reloaded {ext}')
                except Exception as error:
                    await ctx.channel.send(f"An error occurred while Reloading {ext}. See details below:\n```\n{error}\n```")

        @self.command(name='load-cogs', description='Load cogs')
        @commands.has_permissions(administrator=True)
        async def load_cogs(ctx: commands.Context, *args) -> None:
            for ext in args:
                await ctx.channel.send(await self.load(self.cogs_base + ext))

        @self.command(name='unload-cogs', description='Unload cogs')
        @commands.has_permissions(administrator=True)
        async def unload_cogs(ctx: commands.Context, *args) -> None:
            for ext in args:
                await ctx.channel.send(await self.unload(self.cogs_base + ext))

        @self.command(name='load-all-cogs', description='Load all cogs in directory')
        @commands.has_permissions(administrator=True)
        async def load_all_cogs(ctx: commands.Context) -> None:
            for dirpath, _, fnames in os.walk(self.cogs_dir):
                for fname in fnames:
                    if fname.endswith('.py'):
                        fname = os.path.splitext(fname)[0]
                        ext = os.path.join(dirpath, fname).replace(os.sep, '.')
                        await ctx.channel.send(await self.load(ext))

        @self.command(name='unload-all-cogs', description='Unload all loaded cogs')
        @commands.has_permissions(administrator=True)
        async def unload_all_cogs(ctx: commands.Context) -> None:
            while len(self.coglist):
                await ctx.channel.send(await self.unload(self.coglist[0]))

        @self.command(name='show-cogs', description='Display all loaded cogs')
        @commands.has_permissions(administrator=True)
        async def show_cogs(ctx: commands.Context) -> None:
            output = "\n".join(
                self.coglist) if self.coglist else "No cogs loaded"
            await ctx.channel.send(f'```\n{output}\n```')

        @self.command(name='list-cogs', description='Display all available cogs')
        @commands.has_permissions(administrator=True)
        async def list_cogs(ctx: commands.Context) -> None:
            output = ''
            for dirpath, _, fnames in os.walk(self.cogs_dir):
                for fname in fnames:
                    if fname.endswith('.py'):
                        fname = os.path.splitext(fname)[0]
                        dirpath = dirpath[len(self.cogs_dir):]
                        path = os.path.join(
                            dirpath, fname).replace(os.sep, '.')
                        output += '\n' + path
            await ctx.channel.send(f'```\n{output}\n```')

<<<<<<< HEAD
=======
        @self.command(name="sync") 
        async def sync(ctx: commands.Context):
            synced = await self.tree.sync()
            await ctx.channel.send(f"Synced {len(synced)} command(s).")

>>>>>>> 89908d9 (fixed to adapt new openai api)
    async def on_ready(self):
        print('Bot ready as', self.user)

    async def load(self, ext) -> str:
        try:
            await self.load_extension(ext)
            self.coglist.append(ext)
            return f'Loaded {ext}'
        except Exception as error:
            return f"An error occurred while Loading {ext}. See details below:\n```\n{error}\n```"

    async def unload(self, ext) -> str:
        try:
            self.coglist.remove(ext)
            await self.unload_extension(ext)
            return f'Unloaded {ext}'
        except Exception as error:
            return f"An error occurred while Unloading {ext}. See details below:\n```\n{error}\n```"
