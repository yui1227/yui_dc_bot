import discord
from wakeonlan import send_magic_packet
from config import Config
from discord import app_commands
from discord.interactions import Interaction

config = Config()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)


@tree.command(name="電腦開機",
              description="開電腦")
async def openpc(interaction: Interaction):
    if interaction.user.id != config.GetAuthorId():
        await interaction.response.send_message("你不是作者，不能開:P", ephemeral=True)
        return
    await interaction.response.send_message("正在嘗試開電腦...", ephemeral=True)
    send_magic_packet(config.GetPCMAC())


@bot.event
async def on_ready():
    slash = await tree.sync(guild=discord.Object(config.GetMainServerID()))
    print(f'已經以 {bot.user} 登入')
    print(f'已載入 {len(slash)} 個斜線指令')

bot.run(config.GetDcToken())
