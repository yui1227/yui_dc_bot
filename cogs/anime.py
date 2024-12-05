from discord.ext import commands
from discord import Object, Message
from yuidcbot import YuiDcBot
import aiohttp
import re
import json


class Anime(commands.Cog):
    BASE_URL = "https://ani.gamer.com.tw/party.php"

    def __init__(self, bot: YuiDcBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot or not message.content.startswith(self.BASE_URL):
            return
        async with aiohttp.ClientSession() as session:
            async with session.get(message.content) as response:
                html = await response.text()
                # 使用正則抓取資訊
                find: str = re.findall(r"window\.videoList = .+", html)[0]
                # 去除前面文字和最後的分號
                find = find.replace("window.videoList = ", "")[:-1]
                infojson: list = json.loads(find)
                await message.reply(f"""動畫派對: {infojson[0]["title"]}""")


async def setup(bot: YuiDcBot):
    ids = [Object(id) for id in bot.config.GetRunServerID()]
    await bot.add_cog(Anime(bot), guilds=ids)
