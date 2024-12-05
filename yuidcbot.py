from typing import Any
import discord
from discord.ext import commands
from config import Config
from os import listdir


class YuiDcBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True
        self.config = Config()
        self.cog_list = [
            f"cogs.{cogName[:-3]}" for cogName in listdir("cogs") if cogName.endswith(".py")]
        super().__init__("/", intents=intents)

    async def on_ready(self):
        for id in self.config.GetRunServerID():
            slash = await self.tree.sync(guild=discord.Object(id))
            print(f'已載入 {len(slash)} 個斜線指令')
        print(f'已經以 {self.user} 登入')

    async def on_error(self, event_method: str, /, *args: Any, **kwargs: Any) -> None:
        print("ERROR")
        print(event_method)
        print(args)
        print(kwargs)
