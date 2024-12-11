from typing import Any
from discord import Intents, Object, Message, User
from discord.ext import commands
from config import Config
from os import listdir
import traceback
import json
import re
import aiohttp


class YuiDcBot(commands.Bot):
    MESSAGE_REPOST_PATTERN = [
        "https://twitter.com",
        "https://x.com",
        "https://pixiv.net",
        "https://www.pixiv.net",
        "https://bsky.app"
    ]
    ANIME_BASE_URL = "https://ani.gamer.com.tw/party.php"

    def __init__(self):
        intents = Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True
        self.config = Config()
        self.list_cogs()
        super().__init__("/", intents=intents)

    def list_cogs(self):
        self.cog_list = [
            f"cogs.{cogName[:-3]}" for cogName in listdir("cogs") if cogName.endswith(".py")]

    async def on_ready(self):
        for id in self.config.run_server:
            slash = await self.tree.sync(guild=Object(id))
            print(f'已在 {slash[0].guild.name} 載入 {len(slash)} 個斜線指令')
        print(f'已經以 {self.user} 登入')

    async def on_error(self, event_method: str, /, *args: Any, **kwargs: Any):
        print("ERROR")
        print(event_method)
        print(args)
        print(traceback.format_exc())
        if kwargs:
            print(kwargs)

    async def on_message(self, message: Message):
        # 無視機器人訊息
        if message.author.bot:
            return
        # 私訊轉發給作者
        if message.guild is None:
            user: User = self.get_user(self.config.author)
            await user.send(f"from {message.author.name}\n{message.content}")
            return
        # 某頻道本人訊息轉發到某頻道
        if any([message.content.startswith(baseurl) for baseurl in self.MESSAGE_REPOST_PATTERN]):
            user_list = [obj for obj in self.config.repost_list if message.author.id ==
                         obj["author"] and message.channel.id == obj["from"]]
            if any(user_list):
                channel = self.get_channel(
                    user_list[0]["to"])
                await channel.send(message.content)
            return
        # 動畫派對
        if message.content.startswith(self.ANIME_BASE_URL):
            async with aiohttp.ClientSession() as session:
                async with session.get(message.content) as response:
                    html = await response.text()
                    # 使用正則抓取資訊
                    find: str = re.findall(r"window\.videoList = .+", html)[0]
                    # 去除前面文字和最後的分號
                    find = find.replace("window.videoList = ", "")[:-1]
                    infojson: list = json.loads(find)
                    await message.reply(f"""動畫派對: {infojson[0]["title"]}""", mention_author=False)
            return
