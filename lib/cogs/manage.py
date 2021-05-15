from discord.ext.commands.cog import Cog
from discord.ext.commands import command


class Manage(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("cog running")

    @command(name='reload')
    async def reload(self, ctx):
        """Reloads a module."""
        module = "lib.cogs." + ctx.message.content.split(" ")[-1]
        try:
            self.bot.reload_extension(module)
            await ctx.send(f"Cog {module} reloaded")
        except Exception as e:
            print(e)

    @command(name='load')
    async def load(self, ctx):
        """Reloads a module."""
        module = "lib.cogs." + ctx.message.content.split(" ")[-1]
        try:
            self.bot.load_extension(module)
            await ctx.send(f"Cog {module} loaded")
        except Exception as e:
            print(e)


def setup(bot):
    bot.add_cog(Manage(bot))
