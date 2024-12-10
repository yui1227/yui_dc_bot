from discord.ext import commands
from yuidcbot import YuiDcBot
import discord
import subprocess


class Fun(commands.Cog):
    def __init__(self, bot: YuiDcBot):
        self.bot = bot

    @discord.app_commands.command(name="aot-screenshot", description="看巨人現在演到哪裡")
    async def aot_screenshot(self, interaction: discord.interactions.Interaction):
        await interaction.response.defer(ephemeral=False)
        subprocess.run("ffmpeg -y -i $(~/yt-dlp -g g4zpC0WfNx4) -vframes 1 ./aot.jpg",
                       shell=True, capture_output=True)
        await interaction.followup.send(file=discord.File("./aot.jpg"), ephemeral=False)


async def setup(bot: YuiDcBot):
    ids = [discord.Object(id) for id in bot.config.GetRunServerID()]
    await bot.add_cog(Fun(bot), guilds=ids)
