import discord
from discord.ext import commands
from datetime import datetime

# ==========================
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1455306525286600807  # ID канала
# ==========================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Бот запущен как {bot.user}")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != CHANNEL_ID:
        return

    data = message.content.strip().split("\n")

    if len(data) < 3:
        await message.reply(
            "❌ Формат:\n```"
            "SteamID\n"
            "чсс/чсп\n"
            "Причина"
            "```",
            delete_after=10
        )
        return

    steamid = data[0].strip()
    blacklist = data[1].strip().lower()
    reason = "\n".join(data[2:]).strip()

    if blacklist not in ["чсс", "чсп"]:
        await message.reply(
            "❌ Второй строкой должно быть **чсс** или **чсп**.",
            delete_after=10
        )
        return

    title = "🚫 Черный список состава" if blacklist == "чсс" else "🚫 Черный список проекта"

    embed = discord.Embed(
        title=title,
        color=discord.Color.red(),
        timestamp=datetime.utcnow()
    )

    embed.add_field(
        name="🎮 SteamID",
        value=f"`{steamid}`",
        inline=False
    )

    embed.add_field(
        name="📂 Тип",
        value=blacklist.upper(),
        inline=True
    )

    embed.add_field(
        name="👮 Добавил",
        value=message.author.mention,
        inline=True
    )

    embed.add_field(
        name="📄 Причина",
        value=reason,
        inline=False
    )

    embed.set_thumbnail(url=message.author.display_avatar.url)

    embed.set_footer(text="BlackList System")

    try:
        await message.delete()
    except:
        pass

    await message.channel.send(embed=embed)

    await bot.process_commands(message)


bot.run(TOKEN)