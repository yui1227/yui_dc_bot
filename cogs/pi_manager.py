from discord.ext import commands
from wakeonlan import send_magic_packet
from discord.interactions import Interaction
from config import Config
from discord.ext.commands import Bot
from discord import app_commands
from discord import Embed
import psutil
import datetime


class pi_manager(commands.Cog):
    def __init__(self, bot: Bot, config: Config):
        self.bot = bot
        self.config = config

    @app_commands.command(name="電腦開機", description="開電腦")
    async def openpc(self, interaction: Interaction):
        if interaction.user.id != self.config.GetAuthorId():
            await interaction.response.send_message("你不是作者，不能開:P", ephemeral=True)
            return
        await interaction.response.send_message("正在嘗試開電腦...", ephemeral=True)
        send_magic_packet(self.config.GetPCMAC())

    @app_commands.command(name='status', description="查看機器人狀態")
    async def status(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        embed = Embed(title='機器人狀態')
        uptime = datetime.datetime.now()-datetime.datetime.fromtimestamp(psutil.boot_time())
        embed.add_field(name="機器人名稱", value=f"{self.bot.user.name}")
        embed.add_field(name="開機時間", value=f"{uptime.seconds} seconds")
        embed.add_field(
            name="Ping", value=f"{round(self.bot.latency*1000)} ms")
        embed.add_field(name="CPU使用率", value=f"{psutil.cpu_percent()} %")
        embed.add_field(
            name="記憶體使用率", value=f"{psutil.virtual_memory().percent} %")
        embed.add_field(
            name="空間使用率", value=f"""{psutil.disk_usage("/").percent} %""")
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="list-emoji", description="列出這個機器人可用的表情符號")
    async def list_emoji(self, interaction: Interaction):
        pass
        # await interaction.response.defer(ephemeral=True)
        # content = ""
        # for emoji in self.bot:
        #     content+=f"{str(emoji)} {emoji.name}"
        # print(content)
        # embed=Embed(title="本機器人可用的表情符號",description=content)
        # await interaction.followup.send(embed=embed)
