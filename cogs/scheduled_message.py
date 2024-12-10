from typing import Callable
from discord.ext import commands, tasks
import datetime
from discord import File, Object
from discord.ext.tasks import LF, Loop
from yuidcbot import YuiDcBot
# from discord.utils import MISSING
from copy import deepcopy
import json


class ScheduledMessage(commands.Cog):
    def __init__(self, bot: YuiDcBot):
        self.bot = bot
        self.tz = datetime.timezone(datetime.timedelta(hours=8))

        # 根據外部檔案設定排程發送訊息
        self.loop: list[Loop[LF]] = []
        with open("scheduled_message.json") as f:
            self._data = json.load(f)

        for item in self._data:
            # 避免閉包引用問題
            temp = deepcopy(item)
            time = datetime.time(**temp["time"], tzinfo=self.tz)

            @tasks.loop(time=time)
            async def callback(copyitem=temp):
                ch = self.bot.get_channel(copyitem["channel"])
                if "file" in copyitem["data"]:
                    await ch.send(copyitem["data"]["content"],
                                  file=File(copyitem["data"]["file"]))
                else:
                    await ch.send(**copyitem["data"])
            # self.loop.append(tasks.Loop[tasks.LF](
            #     callback, MISSING, MISSING, MISSING, time, None, True, temp["name"]))
            self.loop.append(callback)

        _ = [item.start() for item in self.loop]


async def setup(bot: YuiDcBot):
    ids = [Object(id) for id in bot.config.GetRunServerID()]
    await bot.add_cog(ScheduledMessage(bot), guilds=ids)
