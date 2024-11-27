from discord.ext import commands
from discord import Message
from config import Config
from discord.ext.commands import Bot


class repost(commands.Cog):
    def __init__(self, bot: Bot, config: Config):
        self.bot = bot
        self.config = config

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.id != self.config.GetAuthorId():
            return
        for pair in self.config.GetRepostGuildChannelIdPair():
            fs, ts = pair
            if not message.guild.id == fs["server"] or not message.channel.id == fs["channel"]:
                continue
            guild = await self.bot.fetch_guild(ts["server"])
            channel = await guild.fetch_channel(ts["channel"])
            channel.send(message.content)
