from discord.ext.commands import Cog
from discord.ext import commands
import discord
import pprint


class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("cog running")

    async def show_config(self, ctx):
        embed = discord.Embed(title="Current Config", color=0x226fff)
        for key, value in self.bot.conf[ctx.author.id].items():
            if key != 'reminders':
                embed.add_field(name=key, value=(value or "None"), inline=True)
        await ctx.send(embed=embed)

    @commands.group(name='config')
    async def config(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="!config command usage", color=0x226fff)
            embed.add_field(name="!config", value="Show this help message", inline=False)
            embed.add_field(name="!config set pin <pincode>", value="Set the PINCODE value", inline=False)
            embed.add_field(name="!config set state <stateid>", value="Set the state value", inline=False)
            embed.add_field(name="!config set dist <distid>", value="Set the district value", inline=False)
            embed.add_field(name="!config show", value="Show current config", inline=False)
            embed.add_field(name="!config clear", value="Clear the current config", inline=False)
            embed.set_author(name="CowinBOT", icon_url=self.bot.guild.icon_url)
            await ctx.send(embed=embed)

    @config.group(name="set", pass_context=True)
    async def set_c(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="!check command usage", color=0x226fff)
            embed.add_field(name="!config set", value="Show this help message", inline=False)
            embed.add_field(name="!config set pin <pincode>", value="Set the PINCODE value", inline=False)
            embed.add_field(name="!config set state <stateid>", value="Set the state value", inline=False)
            embed.add_field(name="!config set dist <distid>", value="Set the district value", inline=False)
            embed.set_author(name="CowinBOT", icon_url=self.bot.guild.icon_url)
            await ctx.send(embed=embed)

    @set_c.command(name='state')
    async def state(self, ctx, state: str):
        await self.initialize_config(ctx)
        self.bot.conf[ctx.author.id]['state'] = state
        await self.show_config(ctx)

    @set_c.command(name='dist')
    async def dist(self, ctx, dist):
        await self.initialize_config(ctx)
        self.bot.conf[ctx.author.id]['district'] = dist
        await self.show_config(ctx)

    @set_c.command(name='pin')
    async def pin(self, ctx, pincode):
        await self.initialize_config(ctx)
        self.bot.conf[ctx.author.id]['pincode'] = pincode
        await self.show_config(ctx)

    @set_c.command(name='age')
    async def pin(self, ctx, age):
        await self.initialize_config(ctx)
        self.bot.conf[ctx.author.id]['age'] = age
        await self.show_config(ctx)

    @config.command(name='show')
    async def show(self, ctx):
        await self.initialize_config(ctx)
        await self.show_config(ctx)

    @config.command(name='clear')
    async def clear(self, ctx):
        self.bot.conf[ctx.author.id] = {"state": "", "district": "", "pincode": "", 'reminders': {}, 'age': 45}
        embed = discord.Embed(title="Config Cleared", color=0xbf6bf1)
        await ctx.send(embed=embed)

    async def initialize_config(self, ctx):
        if not self.bot.conf.get(ctx.author.id):
            self.bot.conf[ctx.author.id] = {"state": "", "district": "", "pincode": "", 'reminders': {}, 'age': 45}


def setup(bot):
    bot.add_cog(Config(bot))


"""
    !config
    !config set state <state>
    !config set dist <dist>
    !config set pin <pin>
    !config set maxdist <km>
    !config set phone <phone>
    !config show
    !config clear
"""
