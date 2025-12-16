import discord
import re
from response_manager import load_responses, save_responses
import json
import io


with open('discord_secrets') as f:
    TOKEN = f.readline()
    GUILD_ID = int(f.readline())

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

responses = load_responses()
text_ottosei = responses["しの"]

protected_triggers = ["しの"]

@tree.command(
    name="ottosei",
    description="オットセイbotを呼び出します",
    guild=discord.Object(id=GUILD_ID)
)
async def ottosei(interaction: discord.Interaction):
    text = text_ottosei
    await interaction.response.send_message(text)
    print(f"オットセイしました: {text}")


@tree.command(
    name="add_response",
    description="反応を追加",
    guild=discord.Object(id=GUILD_ID)
)
async def add_response(interaction: discord.Interaction, trigger: str, reply: str):
    if trigger in protected_triggers:
        await interaction.response.send_message(
            "このトリガーは追加できません",
            ephemeral=True
        )
        return
    if trigger in responses:
        await interaction.response.send_message(
            "このトリガーは既に存在します",
            ephemeral=True
        )
        return
    responses[trigger] = reply
    save_responses(responses)
    await interaction.response.send_message(
        f"追加しました: `{trigger}` → `{reply}`",
        ephemeral=True
    )


@tree.command(
    name="del_response",
    description="反応を削除",
    guild=discord.Object(id=GUILD_ID)
)
async def del_response(interaction: discord.Interaction, trigger: str):
    if trigger in responses:
        if trigger in protected_triggers:
            await interaction.response.send_message(
                "このトリガーは削除できません",
                ephemeral=True
            )
            return
        del responses[trigger]
        save_responses(responses)
        await interaction.response.send_message(
            f"削除しました: `{trigger}`",
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            "そのトリガーは存在しません",
            ephemeral=True
        )


@tree.command(
    name="edit_response",
    description="反応を編集",
    guild=discord.Object(id=GUILD_ID)
)
async def edit_response(interaction: discord.Interaction, trigger: str, reply: str):
    if trigger in protected_triggers:
        await interaction.response.send_message(
            "このトリガーは編集できません",
            ephemeral=True
        )
        return
    if trigger not in responses:
        await interaction.response.send_message(
            "そのトリガーは存在しません",
            ephemeral=True
        )
        return
    responses[trigger] = reply
    save_responses(responses)
    await interaction.response.send_message(
        f"編集しました: `{trigger}` → `{reply}`",
        ephemeral=True
    )

@tree.command(
    name="list_responses",
    description="反応を一覧表示",
    guild=discord.Object(id=GUILD_ID)
)
async def list_responses(interaction: discord.Interaction):
    response_list = "\n".join([f"`{trigger}` → `{reply}`" for trigger, reply in responses.items()])
    await interaction.response.send_message(
        f"反応一覧:\n{response_list}",
        ephemeral=True
    )



@tree.command(
    name="export_responses",
    description="反応をJSONファイルとしてエクスポート",
    guild=discord.Object(id=GUILD_ID)
)
async def export_responses(interaction: discord.Interaction):
    json_text = json.dumps(
        responses,
        ensure_ascii=False,
        indent=2
    )

    file = discord.File(
        fp=io.StringIO(json_text),
        filename="responses.json"
    )

    await interaction.response.send_message(
        content="responses.json has been exported.",
        file=file,
        ephemeral=True
    )


@tree.command(
    name="import_responses",
    description="JSONファイルから反応をインポート",
    guild=discord.Object(id=GUILD_ID)
)
async def import_responses(
    interaction: discord.Interaction,
    file: discord.Attachment
):
    if not file.filename.endswith(".json"):
        await interaction.response.send_message(
            "JSONファイルをアップロードしてください",
            ephemeral=True
        )
        return

    try:
        raw = await file.read()
        data = json.loads(raw)

        if not isinstance(data, dict):
            raise ValueError("JSON must be an object")

    except Exception as e:
        await interaction.response.send_message(
            f"無効なJSONファイルです: {e}",
            ephemeral=True
        )
        return

    for trigger in protected_triggers:
        data[trigger] = responses[trigger]

    save_responses(data)


@client.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    await tree.sync(guild=guild)
    print(f"ログインしました: {client.user}")


@client.event
async def on_message(message):
    if message.author.bot:
        return

    hits = []
    for trigger, reply in responses.items():
        for match in re.finditer(trigger, message.content):
            hits.append((match.start(), trigger, reply))

    hits.sort(key=lambda x: x[0])
    for _, trigger, reply in hits:
        await message.channel.send(reply)
        print(f"反応しました: {trigger} -> {reply}")

client.run(TOKEN)
