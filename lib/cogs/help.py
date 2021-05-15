from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.utils import get
import discord


class Help(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

    @Cog.listener()
    async def on_ready(self):
        print("cog running")

    @command(name='help')
    async def show_help(self, ctx, cmd=None):
        embed = discord.Embed(title="Help command", color=0xf0a12c)
        embed.add_field(name="!list", value="List states/districts. Run `!list` for more info", inline=False)
        embed.add_field(name="!check", value="Check vaccine availability in a state/district. Run `!check` for more info", inline=False)
        embed.add_field(name="!remind", value="Start a reminder that checks vaccine availability every N seconds. Run `!remind` for more info", inline=False)
        embed.add_field(name="!config", value="Set the configuration for current user. Run `!config` for more info", inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))