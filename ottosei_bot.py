import discord
import os

with open('discord_token') as f:
    TOKEN = f.readline()
CHANNELID = int(os.getenv('DISCORD_CHANNEL_ID'))

intents = discord.Intents.default()
intents.message_content = True  # ★必須
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"ログインしました: {client.user}")

@client.event
async def on_message(message):
    # Botの発言は無視（無限ループ防止）
    if message.author.bot:
        return

    # 空メッセージ（スタンプ・画像のみ等）を無視
    text = message.content.strip()
    if not text:
        return

    channel = client.get_channel(CHANNELID)
    if channel is None:
        return  # チャンネル未取得時の保険

    await channel.send(text)
    print(text)

client.run(TOKEN)
