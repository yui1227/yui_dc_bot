from typing import Optional
from discord.ext import commands
from yuidcbot import YuiDcBot
from discord import Interaction, app_commands, File, Object, ui, ButtonStyle, Embed
from asyncio import subprocess
import io
from random import choice
import aiohttp


class DeleteButton(ui.View):
    @ui.button(label="刪除", style=ButtonStyle.red)
    async def DeleteMessage(self, interaction: Interaction, button: ui.Button):
        await interaction.message.delete()


class Fun(commands.Cog):
    def __init__(self, bot: YuiDcBot):
        self.bot = bot
        self.aot_ss_cmd = "ffmpeg -y -i $(~/yt-dlp -g g4zpC0WfNx4) -vframes 1 -f image2pipe -vcodec mjpeg pipe:1"
        self.xkcd_apiurl = "https://xkcd.tw/api/strips.json"
        self.xkcd_baseurl = "https://xkcd.tw/"

    @app_commands.command(name="aot-screenshot", description="看巨人現在演到哪裡")
    async def aot_screenshot(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=False)
        proc = await subprocess.create_subprocess_shell(self.aot_ss_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        image_data, error = await proc.communicate()
        if proc.returncode != 0:
            await interaction.followup.send(f"ffmpeg error: {error.decode()}", ephemeral=False)
            return
        byteio = io.BytesIO(image_data)
        await interaction.followup.send(file=File(byteio, filename="aot.jpg"), ephemeral=False, view=DeleteButton())

    @app_commands.command(name="xkcd", description="給你一個xkcd漫畫，未輸入或是輸入錯誤編號則隨機一則")
    async def xkcd(self, interaction: Interaction, xkcd_id: Optional[int] = -1):
        await interaction.response.defer(ephemeral=True)
        async with aiohttp.request('GET', self.xkcd_apiurl) as resp1:
            all_meme: dict = await resp1.json()
            random_meme = all_meme.get(f"{xkcd_id}")
            if random_meme == None:
                all_meme_list = [v for _, v in all_meme.items()]
                random_meme = choice(all_meme_list)
        embed = Embed(title=random_meme["title"],
                      url=f"https://xkcd.tw/{random_meme['id']}",
                      description=random_meme['caption'])
        embed.set_image(url=f"https://xkcd.tw{random_meme['img_url']}")
        await interaction.followup.send(embed=embed)


async def setup(bot: YuiDcBot):
    ids = [Object(id) for id in bot.config.run_server]
    await bot.add_cog(Fun(bot), guilds=ids)
