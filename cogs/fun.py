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
        proc = subprocess.Popen("""
ffmpeg -y -i $(~/yt-dlp -g g4zpC0WfNx4) -vframes 1 -f image2pipe -vcodec mjpeg pipe:1
""", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        image_data, error = proc.communicate()
        if proc.returncode != 0:
            print("err")
            await interaction.followup.send(f"ffmpeg error: {error}", ephemeral=False)
            return
        byteio = io.BytesIO(image_data)
        await interaction.followup.send(file=File(byteio, filename="aot.jpg"), ephemeral=False)


async def setup(bot: YuiDcBot):
    ids = [Object(id) for id in bot.config.run_server]
    await bot.add_cog(Fun(bot), guilds=ids)
