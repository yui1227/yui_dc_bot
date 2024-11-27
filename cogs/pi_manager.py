from discord.ext import commands
from wakeonlan import send_magic_packet
from discord.interactions import Interaction
from config import Config
from discord.ext.commands import Bot


class pi_manager(commands.Cog):
    def __init__(self, bot: Bot, config: Config):
        self.bot = bot
        self.config = config

    @commands.command(name="電腦開機", description="開電腦")
    async def openpc(self, interaction: Interaction):
        if interaction.user.id != self.config.GetAuthorId():
            await interaction.response.send_message("你不是作者，不能開:P", ephemeral=True)
            return
        await interaction.response.send_message("正在嘗試開電腦...", ephemeral=True)
        send_magic_packet(self.config.GetPCMAC())
