from discord.ext import tasks
from discord.ext.commands.cog import Cog
from discord.ext import commands
import discord
import datetime
from log import LOGGER


class Remind(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("cog running")

    @commands.group(name="remind")
    async def remind(self, ctx):
        await self.initialize_config(ctx)
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="!remind command usage", color=0x226fff)
            embed.add_field(name="!remind", value="Show this help message", inline=False)
            embed.add_field(name="!remind pin <pincode> <seconds>", value="Set reminder for pin evey N seconds", inline=False)
            embed.add_field(name="!remind dist <dist> <seconds>", value="Set reminder for dist evey N seconds", inline=False)
            embed.add_field(name="!remind show", value="Show all running reminders", inline=False)
            embed.add_field(name="!remind stop <distid || pincode>", value="Stop reminder with id <distid || pincode>", inline=False)
            embed.add_field(name="!remind stop all", value="Stop all reminders", inline=False)
            embed.set_author(name="CowinBOT", icon_url=self.bot.guild.icon_url)
            await ctx.send(embed=embed)

    @remind.command(name='dist')
    async def dist(self, ctx, dist_id=None, seconds=300):
        if not dist_id:
            dist_id = self.bot.conf.get(ctx.author.id).get('district')
        if (reminders := self.bot.conf[ctx.author.id]['reminders']).get(dist_id):
            if reminders.get(dist_id).remindme.is_running():
                embed = discord.Embed(title="Reminder is already running", color=0xbf6bf1)
                await ctx.send(embed=embed)
                return
            else:
                reminders.pop(dist_id)
        new_reminder = RemindLoop(self.bot, seconds)
        reminders[dist_id] = new_reminder
        new_reminder.remindme.start(ctx=ctx, dist_id=dist_id, seconds=seconds)
        new_reminder.remindme.change_interval(seconds=seconds)
        embed = discord.Embed(title=f"Reminder for {dist_id} running every {seconds} seconds", color=0xbf6bf1)
        await ctx.send(embed=embed)

    @remind.command(name='pin')
    async def dist(self, ctx, pin=None, seconds=300):
        if not pin:
            pin = self.bot.conf.get(ctx.author.id).get('pincode')
        if (reminders := self.bot.conf[ctx.author.id]['reminders']).get(pin):
            if reminders.get(pin).remindme.is_running():
                embed = discord.Embed(title="Reminder is already running", color=0xbf6bf1)
                await ctx.send(embed=embed)
                return
            else:
                reminders.pop(pin)
        new_reminder = RemindLoop(self.bot, seconds)
        reminders[pin] = new_reminder
        new_reminder.remindme.start(ctx=ctx, id=pin, seconds=seconds, dist=False)
        new_reminder.remindme.change_interval(seconds=seconds)
        embed = discord.Embed(title=f"Reminder for {pin} running every {seconds} seconds", color=0xbf6bf1)
        await ctx.send(embed=embed)

    @remind.command(name='show')
    async def show(self, ctx):
        await self.show_reminders(ctx)

    @remind.command(name='stop')
    async def remindstop(self, ctx, arg):
        reminders = self.bot.conf[ctx.author.id]['reminders']
        if arg == 'all':
            for key, value in reminders.items():
                value.remindme.stop()
            self.bot.conf[ctx.author.id]['reminders'] = {}
            embed = discord.Embed(title=f"All reminders stopped", color=0x1ffb11)
            await ctx.send(embed=embed)
        else:
            if arg in reminders:
                reminders[arg].remindme.stop()
                embed = discord.Embed(title=f"Reminder {arg} stopped", color=0x1ffb11)
                await ctx.send(embed=embed)
                reminders.pop(arg)
            else:
                embed = discord.Embed(title=f"Reminder {arg} not found", color=0x1c1b1a)
                await ctx.send(embed=embed)

    async def initialize_config(self, ctx):
        if config := self.bot.conf.get(ctx.author.id):
            if not config.get('reminders'):
                config['reminders'] = {}

    async def show_reminders(self, ctx):
        reminders = self.bot.conf[ctx.author.id]['reminders']
        embed = discord.Embed(title="Running Reminders", color=0x226fff)
        for key, value in reminders.items():
            embed.add_field(name=key, value=f"Every {value.seconds} seconds", inline=True)
        await ctx.send(embed=embed)


class RemindLoop:
    def __init__(self, bot, seconds=300):
        self.bot = bot
        self.seconds = seconds

    @tasks.loop(seconds=300)
    async def remindme(self, ctx, id, seconds=120, dist=True):
        print("Checking for slot availability")
        if 0 < datetime.datetime.now(datetime.timezone.utc)\
                .astimezone(datetime.timezone(datetime.timedelta(hours=5,minutes=30))).hour < 7:
            self.remindme.change_interval(seconds=60*60*1)
        else:
            self.remindme.change_interval(seconds=seconds)
        if dist:
            await self.bot.cogs.get('Check').dist(ctx, id, no_slot_alert=True)
        else:
            await self.bot.cogs.get('Check').pin(ctx, id, no_slot_alert=True)


def setup(bot):
    bot.add_cog(Remind(bot))


"""
    !remind
    !remind dist <state> <dist1>,<dist2> <frequency>
    !remind pin <pincode> <frequency>
    !remind show
    !remind clear
    !remind remove <id>
"""
