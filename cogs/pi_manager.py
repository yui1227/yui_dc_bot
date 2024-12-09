from discord.ext import commands
from wakeonlan import send_magic_packet
from discord.interactions import Interaction
from discord import app_commands, Embed, Object
import discord
import psutil
import datetime
from yuidcbot import YuiDcBot


class PiManager(commands.Cog):
    def __init__(self, bot: YuiDcBot):
        self.bot = bot

    @app_commands.command(name="電腦開機", description="開電腦")
    async def openpc(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        if interaction.user.id != self.bot.config.GetAuthorId():
            await interaction.followup.send("你不是作者，不能開:P", ephemeral=True)
            return
        await interaction.followup.send("正在嘗試開電腦...", ephemeral=True)
        send_magic_packet(self.bot.config.GetPCMAC())

    @app_commands.command(name='status', description="查看機器人狀態")
    async def status(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        embed = Embed(title='機器人狀態')
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        uptime = datetime.datetime.now()-datetime.datetime.fromtimestamp(psutil.boot_time())
        embed.add_field(name="機器人名稱", value=f"{self.bot.user.name}")
        embed.add_field(name="Discord.py 版本", value=f"{discord.__version__}")
        embed.add_field(name="開機時間", value=f"{uptime.seconds} seconds")
        embed.add_field(
            name="Ping", value=f"{round(self.bot.latency*1000)} ms")
        embed.add_field(name="CPU使用率", value=f"{psutil.cpu_percent()} %")
        embed.add_field(
            name="記憶體使用率", value=f"{psutil.virtual_memory().percent} %")
        embed.add_field(
            name="空間使用率", value=f"""{psutil.disk_usage("/").percent} %""")
        await interaction.followup.send(embed=embed)


async def setup(bot: YuiDcBot):
    ids = [Object(id) for id in bot.config.GetRunServerID()]
    await bot.add_cog(PiManager(bot), guilds=ids)
