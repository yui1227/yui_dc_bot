from discord.ext import commands, tasks
import datetime
from config import Config
from discord.ext.commands import Bot

utcp8 = datetime.timezone(datetime.timedelta(hours=8))

am3 = datetime.time(hour=3, tzinfo=utcp8)
am4 = datetime.time(hour=4, tzinfo=utcp8)


class am3am4(commands.Cog):
    def __init__(self, bot: Bot, config: Config):
        self.bot = bot
        self.config = config

    @tasks.loop(time=am3)
    async def am3(self):
        pass

    @tasks.loop(time=am4)
    async def am4(self):
        pass