import discord
import random
from discord.ext.commands import Bot as BotBase
from discord import Intents
from glob import glob
from log import LOGGER

__author__ = "Febin Jose"

PREFIX = "!"
OWNER_IDS = [608587691533271042]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.stdout = None
        self.TOKEN = None
        self.VERSION = None
        self.conf = {OWNER_IDS[0]:{"state": "", "district": "", "pincode": ""}}
        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS, intents=Intents.all())

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            LOGGER.debug(f"{cog} cog loaded")
        LOGGER.debug("setup complete")

    def run(self, version):
        self.VERSION = version
        LOGGER.debug('Running setup')
        self.setup()
        with open('./lib/bot/token.0', 'r', encoding="utf-8") as tf:
            self.TOKEN = tf.read().strip()
        LOGGER.info("Running bot")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        LOGGER.info(f'{self.user} has connected to Discord!')
        LOGGER.debug(self.guilds)
        for guild in self.guilds:
            members = '\n - '.join([member.name for member in guild.members])
            LOGGER.debug(f'Guild Members:\n - {members}')

    @staticmethod
    async def on_disconnect():
        LOGGER.info("Bot disconnected")

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(764435868453830656)
            self.stdout = self.get_channel(839197254283690034)
            brooklyn_99_quotes = [
                'I\'m the human form of the 💯 emoji.',
                'Bingpot!',
                (
                    'Cool. Cool cool cool cool cool cool cool, '
                    'no doubt no doubt no doubt no doubt.'
                ),
            ]
            embed = discord.Embed(title="Now Online", description=f"Version {self.VERSION}", color=0xaf630f)
            for i in range(3):
                embed.add_field(name=str(i), value=random.choice(brooklyn_99_quotes), inline=False)
            embed.set_author(name="CowinBOT", icon_url=self.guild.icon_url)
            await self.stdout.send(embed=embed)
            LOGGER.info("Bot ready")
            self.ready = True
        else:
            LOGGER.info("Bot disconnected")

    async def print_message(self):
        await self.stdout.send("Time Notification")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await self.stdout.send("Something went wrong")
        else:
            await self.stdout.send("An error occurred")
        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, discord.ext.commands.errors.CheckFailure):
            await ctx.send('You do not have the correct role for this command.')
        elif isinstance(exc, discord.ext.commands.errors.CommandNotFound):
            await ctx.send('No Such command')
        elif hasattr(exc, "original"):
            raise exc.original
        else:
            raise exc

    @staticmethod
    async def cog_command_error(ctx, exc):
        if isinstance(exc, discord.ext.commands.errors.CheckFailure):
            await ctx.send('You do not have the correct role for this command.')
        elif isinstance(exc, discord.ext.commands.errors.CommandNotFound):
            await ctx.send('No Such command')
        elif hasattr(exc, "original"):
            raise exc.original
        else:
            raise exc


bot = Bot()
