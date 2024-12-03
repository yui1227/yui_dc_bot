from discord.ext import commands
from discord import Message, User, Object
from yuidcbot import YuiDcBot


class repost(commands.Cog):
    REPOST_PATTERN = [
        "https://twitter.com",
        "https://x.com",
        "https://pixiv.net",
        "https://www.pixiv.net",
        "https://bsky.app"
    ]

    def __init__(self, bot: YuiDcBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        # DM Forward
        if not message.author.bot and message.guild is None:
            user: User = await self.bot.fetch_user(self.bot.config.GetAuthorId())
            await user.send(f"from {message.author.name}\n{message.content}", embeds=message.embeds, stickers=message.stickers)
            return
        if message.author.id != self.bot.config.GetAuthorId():
            return
        if not any([message.content.startswith(baseurl) for baseurl in self.REPOST_PATTERN]):
            return
        # Message Forward to another message
        for pair in self.bot.config.GetRepostGuildChannelIdPair():
            fs, ts = pair
            if not message.guild.id == fs["server"] or not message.channel.id == fs["channel"]:
                continue
            guild = await self.bot.fetch_guild(ts["server"])
            channel = await guild.fetch_channel(ts["channel"])
            await channel.send(message.content)


async def setup(bot: YuiDcBot):
    ids = [Object(id) for id in bot.config.GetRunServerID()]
    await bot.add_cog(repost(bot), guilds=ids)
