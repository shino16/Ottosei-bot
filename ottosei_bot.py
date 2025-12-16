import discord
import re

with open('discord_secrets') as f:
    TOKEN = f.readline()
    GUILD_ID = int(f.readline())

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

text_ottosei = "オットセイの真似しまーすｗｗｗおうおうおうおうおｗｗwｗパァンッパァンッ(ヒレを叩く音)おうおうおうおうおうおうおｗｗｗｗパァンッパァンッ(ヒレを叩く音)ｗｗｗｗおうおうおうおうおうおｗｗｗｗｗパァンッパァンッ(ヒレを叩く音)ｗｗｗｗおうおうおうおうおうおｗｗｗｗｗパァンッパ"

@client.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    await tree.sync(guild=guild)
    print(f"ログインしました: {client.user}")

@tree.command(
    name="ottosei",
    description="オットセイbotを呼び出します",
    guild=discord.Object(id=GUILD_ID)
)
async def ottosei(interaction: discord.Interaction):
    text = text_ottosei
    await interaction.response.send_message(text)
    print(f"オットセイしました: {text}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    responses = {
        "しの": text_ottosei,
        "ぬるぽ": "ｶﾞｯ!",
        "膃肭臍": "膃肭臍の話した？",
        "おっとせい": "おっとせいの話した？",
        "オットセイ": "オットセイの話した？",
    }

    hits = []

    for pattern, reply in responses.items():
        for match in re.finditer(pattern, message.content):
            hits.append((match.start(), reply))

    hits.sort(key=lambda x: x[0])

    for _, reply in hits:
        await message.channel.send(reply)

client.run(TOKEN)
