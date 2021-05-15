import discord
from discord.ext.commands import Cog
from discord.ext import commands
from ..apis import list_api
import textwrap
from log import LOGGER


class List(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.states = {}
        self.dists = {}

    @Cog.listener()
    async def on_ready(self):
        LOGGER.info(f"cog {__name__} running")

    @Cog.listener()
    async def on_error(self):
        pass

    @commands.group(name="list")
    async def list(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="!list command usage", color=0x226fff)
            embed.add_field(name="!list", value="Show this help message", inline=False)
            embed.add_field(name="!list states", value="List all states and its IDs", inline=False)
            embed.add_field(name="!list dist <state>", value="List all districts in the state and its IDs. "
                                                             "Reads <state> from config if set", inline=False)
            embed.add_field(name="!list members <phone>", value="List all states and its IDs", inline=False)
            embed.set_author(name="CowinBOT", icon_url=self.bot.guild.icon_url)
            await ctx.send(embed=embed)

    @list.command(name="states")
    async def state(self, ctx):
        states_data = await list_api.list_states()
        if not states_data:
            await ctx.send("Error fetching states data")
            return
        self.states = {state.get('state_id'): state.get('state_name') for state in states_data}
        embed = discord.Embed(title="States List", color=0xc0dfd1)
        embed.set_author(name="CowinBOT", icon_url=self.bot.guild.icon_url)
        states_data = sorted(states_data, key=lambda x: x['state_id'])
        LOGGER.debug(states_data)
        count = 0
        for state in states_data:
            if count < 24:
                count += 1
                embed.add_field(name=state.get('state_id'), value=state.get('state_name'))
            else:
                await ctx.send(embed=embed)
                embed = discord.Embed(title="States List Cont..", color=0xc0dfd1)
                embed.add_field(name=state.get('state_id'), value=state.get('state_name'))
                count = 1
        if count:
            await ctx.send(embed=embed)

    @list.command(name="dist")
    async def dist(self, ctx, state_input=""):
        if not state_input:
            # check if config for state is set
            await ctx.send("Taking dist from config")
            state_id = "17"
        elif state_input.isdigit():
            if not self.states:
                states_data = await list_api.list_states()
                if not states_data:
                    await ctx.send("Error fetching states data")
                    return
                self.states = {state.get('state_id'): state.get('state_name') for state in states_data}
            if state_input in self.states.values():
                state_id = [key for key, value in self.states.items() if state_input == value][0]
            else:
                state_id = state_input
        else:
            embed = discord.Embed(title="District List Command error. State ID must be an integer", color=0xc0dfd1)
            await ctx.send(embed=embed)
            return

        dist_data = await list_api.list_dist(state_id)
        embed = discord.Embed(title=f"{self.states.get(int(state_input))} District List", color=0xc0dfd1)
        embed.set_author(name="CowinBOT", icon_url=self.bot.guild.icon_url)
        count = 0
        for dist in dist_data:
            if count < 24:
                count += 1
                embed.add_field(name=dist.get('district_id'), value=dist.get('district_name'))
            else:
                await ctx.send(embed=embed)
                embed = discord.Embed(title="District List Cont..", color=0xc0dfd1)
                embed.add_field(name=dist.get('district_id'), value=dist.get('district_name'))
                count = 0
        if count:
            await ctx.send(embed=embed)

    @list.command(name="members")
    async def members(self, ctx, *args):
        if not args:
            # check if config for state is set
            await ctx.send("Taking phone from config")
        else:
            await ctx.send(f"Members for {args[0]}")


def setup(bot):
    bot.add_cog(List(bot))


"""
    !list
    !list state
    !list dist <state>
    !list members <phone>
"""
