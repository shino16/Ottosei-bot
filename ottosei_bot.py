import discord

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

    dict = {
        "しの": text_ottosei,
        "ぬるぽ": "ｶﾞｯ",
        "オットセイ": text_ottosei,
    }

    if message.content and message.content in dict:
        text = dict[message.content]
        await message.channel.send(text)
        print(f"反応しました: {text}")

client.run(TOKEN)
