from discord.ext import commands
from yuidcbot import YuiDcBot
from discord import Interaction, app_commands, File, Object
from asyncio import subprocess
import io
import json
from random import choice


class Fun(commands.Cog):
    def __init__(self, bot: YuiDcBot):
        self.bot = bot
        self.aot_ss_cmd = "ffmpeg -y -i $(~/yt-dlp -g g4zpC0WfNx4) -vframes 1 -f image2pipe -vcodec mjpeg pipe:1"
        with open("resources/million_cards.json") as f:
            self.million_card: list[str] = json.load(f)

    @app_commands.command(name="aot-screenshot", description="看巨人現在演到哪裡")
    async def aot_screenshot(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=False)
        proc = await subprocess.create_subprocess_shell(self.aot_ss_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        image_data, error = await proc.communicate()
        if proc.returncode != 0:
            await interaction.followup.send(f"ffmpeg error: {error.decode()}", ephemeral=False)
            return
        byteio = io.BytesIO(image_data)
        await interaction.followup.send(file=File(byteio, filename="aot.jpg"), ephemeral=False)

    @app_commands.command(name="random-million", description="抽一張百萬卡")
    async def random_million_card(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send(choice(self.million_card), ephemeral=False)


async def setup(bot: YuiDcBot):
    ids = [Object(id) for id in bot.config.run_server]
    await bot.add_cog(Fun(bot), guilds=ids)
