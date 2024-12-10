from discord.ext import commands
from wakeonlan import send_magic_packet
from discord import app_commands, Embed, Object, Interaction
from discord import __version__ as dpyver
import psutil
import datetime
from yuidcbot import YuiDcBot


class PiManager(commands.Cog):
    def __init__(self, bot: YuiDcBot):
        self.bot = bot

    @app_commands.command(name="電腦開機", description="開電腦")
    async def openpc(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        if interaction.user.id != self.bot.config.author:
            await interaction.followup.send("你不是作者，不能開:P", ephemeral=True)
            return
        await interaction.followup.send("正在嘗試開電腦...", ephemeral=True)
        send_magic_packet(self.bot.config.pc_mac)

    @app_commands.command(name='status', description="查看機器人狀態")
    async def status(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        uptime = datetime.datetime.now()-datetime.datetime.fromtimestamp(psutil.boot_time())
        message_pair = [
            ("機器人名稱", self.bot.user.name),
            ("Discord.py 版本", dpyver),
            ("開機時間", f"{uptime.seconds} seconds"),
            ("Ping", f"{round(self.bot.latency*1000)} ms"),
            ("CPU使用率", f"{psutil.cpu_percent()} %"),
            ("記憶體使用率", f"{psutil.virtual_memory().percent} %"),
            ("空間使用率", f"""{psutil.disk_usage("/").percent} %""")
        ]
        embed = Embed(title='機器人狀態')
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        _ = [embed.add_field(name=pair[0], value=pair[1])
             for pair in message_pair]
        await interaction.followup.send(embed=embed)


async def setup(bot: YuiDcBot):
    ids = [Object(id) for id in bot.config.run_server]
    await bot.add_cog(PiManager(bot), guilds=ids)
