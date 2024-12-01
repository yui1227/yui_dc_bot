from discord.ext import commands, tasks
import datetime
from config import Config
from discord.ext.commands import Bot
from discord import File

utcp8 = datetime.timezone(datetime.timedelta(hours=8))

am3 = datetime.time(hour=3, tzinfo=utcp8)
am4 = datetime.time(hour=4, tzinfo=utcp8)


class am3am4(commands.Cog):
    def __init__(self, bot: Bot, config: Config):
        self.bot = bot
        self.config = config
        self.am3.start()
        self.am4.start()

    @tasks.loop(time=am3)
    async def am3(self):
        guild = await self.bot.fetch_guild(69255840699256832)
        ch = await guild.fetch_channel(651043415009787905)
        await ch.send(f"<:am3:1312858058375827549>")

    @tasks.loop(time=am4)
    async def am4(self):
        guild = await self.bot.fetch_guild(69255840699256832)
        ch = await guild.fetch_channel(651043415009787905)
        await ch.send(f"朝の4時よ！これから走りに出るんでしょ？", file=File("resources/4am_jog.mp4"))
