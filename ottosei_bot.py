import discord

with open('discord_secrets') as f:
    TOKEN = f.readline()
    TOKEN = f.readline()
    GUILD_ID = int(f.readline())

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

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
    text = "オットセイの真似しまーすｗｗｗおうおうおうおうおｗｗwｗパァンッパァンッ(ヒレを叩く音)おうおうおうおうおうおうおうおｗｗｗｗパァンッパァンッ(ヒレを叩く音)ｗｗｗｗおうおうおうおうおうおｗｗｗｗｗパァンッパァンッ(ヒレを叩く音)ｗｗｗｗおうおうおうおうおうおｗｗｗｗｗパァンッパ"
    await interaction.response.send_message(text)

client.run(TOKEN)
