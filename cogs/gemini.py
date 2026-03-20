import discord
from discord import app_commands
from discord.ext import commands
import io
from google import genai
from google.genai import types

from yuidcbot import YuiDcBot

class GeminiFixedPromptCog(commands.Cog):
    def __init__(self, bot: YuiDcBot):
        self.bot = bot
        
        # --- 📝 這裡是你寫死的提示詞 (硬編碼) ---
        # 你可以根據需求修改這裡的文字，例如：
        # "將這張圖片轉換為吉卜力動漫風格"
        # "把這張圖片變成賽博龐克風格的城市"
        # "將圖片中的主角變成寫實風格"
        self.HARDCODED_PROMPT = "將這張圖片轉換為冰天雪地的樣子，並且保持原圖的構圖和主體不變。"
        # -------------------------------------

        # 1. 初始化 Gemini 客戶端
        # 請確保在 bot 主程式中處理了 API_KEY 的安全讀取（例如使用 .env）
        # 這裡為了展示，先假設直接填入或從 main pass 進來
        self.ai_client = genai.Client(api_key=bot.config.gemini)

        # 2. 定義訊息右鍵選單指令 (Message Context Menu)
        self.ctx_menu = app_commands.ContextMenu(
            name='冰起來', # 這是顯示在右鍵選單中的名字
            callback=self.generate_image_context_fixed
        )
        # 將右鍵指令加入到 Bot 的指令樹中
        self.bot.tree.add_command(self.ctx_menu)

    # 當 Cog 被卸載時，自動移除這個右鍵指令，避免錯誤
    async def cog_unload(self):
        self.bot.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)

    # 右鍵指令的實際執行邏輯
    async def generate_image_context_fixed(self, interaction: discord.Interaction, message: discord.Message):
        """
        當使用者對訊息按右鍵選擇指令時觸發
        """
        
        # 1. 基礎檢查：訊息是否有附件
        if not message.attachments:
            # ephemeral=True 代表回應只有點擊的使用者看得到，不打擾頻道其他人
            await interaction.response.send_message("❌ 這則訊息沒有包含任何圖片附件喔！", ephemeral=True)
            return

        attachment = message.attachments[0]
        
        # 2. 基礎檢查：附件是否為圖片
        if not attachment.content_type or not attachment.content_type.startswith('image/'):
            await interaction.response.send_message("❌ 抓到的附件不是圖片格式！", ephemeral=True)
            return

        # 3. 檢查通過，告訴 Discord 機器人正在處理中（這會顯示「應用程式正在思考...」）
        # 因生圖需要時間，必須先呼叫 defer() 避免 interaction 超時 (3秒)
        await interaction.response.defer(thinking=True)

        try:
            # 4. 讀取 Discord 上的圖片並轉換為 bytes
            # 此步驟為非同步，不會卡住 bot
            image_bytes = await attachment.read()
            mime_type = attachment.content_type

            # 5. 呼叫 Gemini API (使用非同步 .aio 客戶端)
            # 使用 gemini-2.0-flash 模型，支援原生的 IMAGE 輸出
            response = await self.ai_client.aio.models.generate_content(
                model='gemini-2.0-flash', 
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type=mime_type), # 輸入的原圖
                    self.HARDCODED_PROMPT # 使用我們寫死的固定提示詞
                ],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"] # 關鍵：強制模型回傳圖片而非文字
                )
            )

            # 6. 解析與驗證 Gemini 回傳的結果
            if not response.candidates or not response.candidates[0].content.parts:
                await interaction.followup.send("❌ Gemini 處理完成但沒有回傳圖片內容，請稍後再試。")
                return

            output_part = response.candidates[0].content.parts[0]
            
            # 檢查模型是否成功生成了圖片二進制資料
            if output_part.inline_data and output_part.inline_data.data:
                output_bytes = output_part.inline_data.data
                
                # 7. 將生成的圖片 bytes 轉為 Discord File 物件
                result_file = discord.File(io.BytesIO(output_bytes), filename="gemini_generated.png")
                
                # 將圖片作為 followup (後續回應) 傳回頻道
                await interaction.followup.send(
                    content=f"{interaction.user.mention} 處理完成！\n 👉 原圖來源：{message.jump_url}", 
                    file=result_file
                )
            else:
                # 預防機制：如果模型因為安全過濾或其他原因只回傳了文字 (refusal)
                text_response = output_part.text if output_part.text else "模型拒絕生成圖片且未提供原因。"
                await interaction.followup.send(f"⚠️ 模型無法依據原圖生成新圖片，回傳了文字說明：\n`{text_response}`")

        except Exception as e:
            # 捕捉所有未預期的錯誤並通知使用者
            print(f"Error in GeminiFixedPromptCog: {e}")
            await interaction.followup.send(f"❌ 處理過程中發生錯誤：{e}")

# Cog 載入函式
async def setup(bot: YuiDcBot):
    ids = [discord.Object(id) for id in bot.config.run_server]
    await bot.add_cog(GeminiFixedPromptCog(bot), guilds=ids)