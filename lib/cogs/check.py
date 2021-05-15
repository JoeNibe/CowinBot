from discord.ext.commands.cog import Cog
from discord.ext import commands
import discord
import datetime
from ..apis import check_api
from log import LOGGER


class Check(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        LOGGER.info("cog {name} running")

    @commands.group(name="check")
    async def check(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="!check command usage", color=0x226fff)
            embed.add_field(name="!check", value="Show this help message", inline=False)
            embed.add_field(name="!check pin <pincode>", value="Check vaccine availability at PINCODE", inline=False)
            embed.add_field(name="!check dist <distid>", value="Check vaccine availability in district", inline=False)
            embed.set_author(name="CowinBOT", icon_url=self.bot.guild.icon_url)
            await ctx.send(embed=embed)

    @check.command(name="pin")
    async def pin(self, ctx, pincode, no_slot_alert=True):
        date = datetime.datetime.now(datetime.timezone.utc)\
            .astimezone(datetime.timezone(datetime.timedelta(hours=5,minutes=30))).strftime("%d-%m-%Y %H:%M:%S")
        pin_data = await check_api.check_pin(pincode, date)
        await self.send_message(ctx, pin_data, no_slot_alert=no_slot_alert)

    @check.command(name="dist")
    async def dist(self, ctx, dist_id, no_slot_alert=True):
        date = datetime.datetime.now(datetime.timezone.utc)\
            .astimezone(datetime.timezone(datetime.timedelta(hours=5,minutes=30))).strftime("%d-%m-%Y %H:%M:%S")
        dist_data = await check_api.check_dist(dist_id, date)
        await self.send_message(ctx, dist_data, no_slot_alert=no_slot_alert)

    async def send_message(self, ctx, data, no_slot_alert=True):
        embed = discord.Embed(title="Available Slots", color=0xccaf1f)
        embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc)
                         .astimezone(datetime.timezone(datetime.timedelta(hours=5,minutes=30))).strftime("%d-%m-%Y %H:%M:%S"))
        count = 0
        age = int(self.bot.conf[ctx.author.id]['age']) or 45
        available = False
        mention_user = True
        for center in data:
            for session in center.get('sessions'):
                if session.get('available_capacity') >= 1 and session.get('min_age_limit') <= age:
                    available = True
                    availability_data = f"```Date: {session.get('date')}\nVaccine: {session.get('vaccine')}\n" \
                                        f"Min Age: {session.get('min_age_limit')}\n" \
                                        f"Available Slots: {session.get('available_capacity')}\n" \
                                        f"Fee Type: {center.get('fee_type')}\n" \
                                        f"Slots: {session.get('slots')}```"
                    embed.add_field(name=f"{count + 1}. {center.get('name')}, {center.get('pincode')}\n "
                                         f"```{center.get('address')}```", value=availability_data, inline=False)
                    count += 1
                    if count == 24 or len(embed) > 5400:
                        if mention_user:
                            await ctx.send(f'<@{ctx.author.id}> Vaccine is available. Please book ASAP')
                        await ctx.send(embed=embed)
                        mention_user = False
                        embed = discord.Embed(title="Available Slots Cont...", color=0xccaf1f)
                        embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc)
                                         .astimezone(datetime.timezone(datetime.timedelta(hours=5,minutes=30))).strftime("%d-%m-%Y %H:%M:%S"))
                        count = 0
        if not data or not available:
            if no_slot_alert:
                embed = discord.Embed(title="No Slots available", color=0xe111cc)
                embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc)
                                 .astimezone(datetime.timezone(datetime.timedelta(hours=5,minutes=30)))
                                 .strftime("%d-%m-%Y %H:%M:%S"))
                await ctx.send(embed=embed)
            return
        if mention_user:
            await ctx.send(f'<@{ctx.author.id}> Vaccine is available. Please book ASAP')
        if count:
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Check(bot))


"""
    !check
    !check pin <pin>
    !check dist <state> <dist>
"""
