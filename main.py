import discord
from config import Config
from discord.ext import commands
from discord.interactions import Interaction
from cogs.pi_manager import pi_manager
from cogs.am3am4 import am3am4
from cogs.repost import repost

config = Config()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="/",intents=intents)


@bot.event
async def on_ready():
    await bot.add_cog(pi_manager(bot, config))
    await bot.add_cog(am3am4(bot, config))
    await bot.add_cog(repost(bot, config))
    for id in config.GetRunServerID():
        slash = await bot.tree.sync(guild=discord.Object(id))
        print(f'已經以 {bot.user} 登入')
        print(f'已載入 {len(slash)} 個斜線指令')

bot.run(config.GetDcToken())
