from yuidcbot import YuiDcBot
import asyncio
from discord.interactions import Interaction
from discord import Object

bot = YuiDcBot()


@bot.tree.command(name="reload", description="重整模組", guilds=[Object(id) for id in bot.config.GetRunServerID()])
async def reload(interaction: Interaction):
    await interaction.response.defer(ephemeral=True)
    if interaction.user.id != bot.config.GetAuthorId():
        await interaction.followup.send("你不是作者，不能開:P", ephemeral=True)
        return
    await interaction.followup.send("正在重整模組...", ephemeral=True)
    for cogs in bot.cog_list:
        await bot.reload_extension(cogs)
    await interaction.followup.send("重整模組完畢", ephemeral=True)


async def main():
    async with bot:
        for cogs in bot.cog_list:
            await bot.load_extension(cogs)
        await bot.start(bot.config.GetDcToken())

if __name__ == "__main__":
    asyncio.run(main())
