from discord.ext import commands
from yuidcbot import YuiDcBot
from discord import Interaction, app_commands, File, Object
import subprocess
import io

class Fun(commands.Cog):
    def __init__(self, bot: YuiDcBot):
        self.bot = bot

    @app_commands.command(name="aot-screenshot", description="看巨人現在演到哪裡")
    async def aot_screenshot(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=False)
        subprocess.run("ffmpeg -y -i $(~/yt-dlp -g g4zpC0WfNx4) -vframes 1 ./aot.jpg",
                       shell=True, capture_output=True)
        await interaction.followup.send(file=File("./aot.jpg"), ephemeral=False)


async def setup(bot: YuiDcBot):
    ids = [Object(id) for id in bot.config.run_server]
    await bot.add_cog(Fun(bot), guilds=ids)
