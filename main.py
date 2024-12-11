from yuidcbot import YuiDcBot
import asyncio
from discord import Object, Interaction

bot = YuiDcBot()


@bot.tree.command(name="reload", description="卸載現有模組並重新載入模組以及載入新模組", guilds=[Object(id) for id in bot.config.run_server])
async def reload(interaction: Interaction):
    await interaction.response.defer(ephemeral=True)
    if interaction.user.id != bot.config.author:
        await interaction.followup.send("你不是作者，不能開:P", ephemeral=True)
        return
    await interaction.followup.send("正在重整模組...", ephemeral=True)

    for cogs in bot.cog_list:
        await bot.unload_extension(cogs)
    await interaction.followup.send("已卸載以下插件:\n"+"\n".join(bot.cog_list), ephemeral=True)

    bot.list_cogs()
    for cogs in bot.cog_list:
        await bot.load_extension(cogs)
    await interaction.followup.send("已載入以下插件:\n"+"\n".join(bot.cog_list), ephemeral=True)

    for id in bot.config.run_server:
        slash = await bot.tree.sync(guild=Object(id))
        print(f'已在 {slash[0].guild.name} 載入 {len(slash)} 個斜線指令')

    await interaction.followup.send("重整模組完畢", ephemeral=True)


async def main():
    async with bot:
        for cogs in bot.cog_list:
            await bot.load_extension(cogs)
        await bot.start(bot.config.dc_token)

if __name__ == "__main__":
    asyncio.run(main())
