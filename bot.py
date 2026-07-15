import os
import discord
from discord.ext import commands


TOKEN = os.getenv("DISCORD_TOKEN")


# ==========================
# НАСТРОЙКИ
# ==========================

REQUEST_CHANNEL_ID = 1454624497314304155  # канал где кнопка создания заявки
CHECK_CHANNEL_ID = 1454624497314304155     # канал куда приходят заявки

CURATOR_ROLE_ID = 1454624496777429091      # куратор
SPECIAL_ROLE_ID = 1475245060017750106      # спешик
PERSONAL_ROLE_ID = 1521380394329571479     # personal

PING_ROLE_ID = 1526612860627718185


# ==========================


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)



# ==========================
# ФОРМА
# ==========================

class AdminRequestModal(discord.ui.Modal, title="👑 Запрос административной роли"):


    nickname = discord.ui.TextInput(
        label="🎮 Ник",
        placeholder="Ваш игровой ник",
        max_length=50
    )


    profile = discord.ui.TextInput(
        label="🔗 Ссылка на профиль",
        placeholder="Ссылка на профиль игрока",
        max_length=300
    )


    rank = discord.ui.TextInput(
        label="⭐ Ранг админки",
        placeholder="Admin / Admin+ / Sponsor",
        max_length=30
    )


    period = discord.ui.TextInput(
        label="📅 Период админки",
        placeholder="10.07.2026 - 25.07.2026",
        max_length=50
    )


    screenshot = discord.ui.TextInput(
        label="📸 Скрин с сайта (профиль)",
        placeholder="Скрин залить на yapx.ru (или другой сайт для скринов) и отправить ссылку",
        max_length=300
    )


    async def on_submit(self, interaction: discord.Interaction):

        channel = bot.get_channel(
            CHECK_CHANNEL_ID
        )


        embed = discord.Embed(
            title="👑 Запрос административной роли",
            color=discord.Color.gold()
        )


        embed.set_author(
            name=str(interaction.user),
            icon_url=interaction.user.display_avatar.url
        )


        embed.add_field(
            name="👤 Автор",
            value=interaction.user.mention,
            inline=False
        )


        embed.add_field(
            name="🎮 Ник",
            value=self.nickname.value,
            inline=False
        )


        embed.add_field(
            name="🔗 Профиль",
            value=self.profile.value,
            inline=False
        )


        embed.add_field(
            name="⭐ Ранг",
            value=self.rank.value,
            inline=False
        )


        embed.add_field(
            name="📅 Период",
            value=self.period.value,
            inline=False
        )


        embed.add_field(
            name="📸 Скрин",
            value=self.screenshot.value,
            inline=False
        )


        embed.set_thumbnail(
            url=interaction.user.display_avatar.url
        )


        await channel.send(
            f"<@&{PING_ROLE_ID}>",
            embed=embed,
            view=AdminButtons()
        )


        await interaction.response.send_message(
            "✅ Заявка отправлена.",
            ephemeral=True
        )



# ==========================
# КНОПКА СОЗДАНИЯ
# ==========================


class CreateRequest(discord.ui.View):

    def __init__(self):
        super().__init__(
            timeout=None
        )


    @discord.ui.button(
        label="📋 Создать запрос",
        style=discord.ButtonStyle.primary
    )
    async def create(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.send_modal(
            AdminRequestModal()
        )



# ==========================
# КНОПКИ ПРОВЕРКИ
# ==========================


class AdminButtons(discord.ui.View):

    def __init__(self):
        super().__init__(
            timeout=None
        )


    def has_access(self, interaction):

        user_roles = [
            role.id
            for role in interaction.user.roles
        ]


        allowed = [
            CURATOR_ROLE_ID,
            SPECIAL_ROLE_ID,
            PERSONAL_ROLE_ID
        ]


        return any(
            role in user_roles
            for role in allowed
        )



    @discord.ui.button(
        label="✅ Одобрить",
        style=discord.ButtonStyle.success
    )
    async def approve(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):


        if not self.has_access(interaction):

            return await interaction.response.send_message(
                "❌ Нет доступа.",
                ephemeral=True
            )


        embed = interaction.message.embeds[0]

        embed.color = discord.Color.green()

        embed.add_field(
            name="✅ Решение",
            value=f"Одобрил: {interaction.user.mention}",
            inline=False
        )


        for item in self.children:
            item.disabled = True


        await interaction.message.edit(
            embed=embed,
            view=self
        )


        await interaction.response.send_message(
            "Заявка одобрена.",
            ephemeral=True
        )



    @discord.ui.button(
        label="❌ Отклонить",
        style=discord.ButtonStyle.danger
    )
    async def reject(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):


        if not self.has_access(interaction):

            return await interaction.response.send_message(
                "❌ Нет доступа.",
                ephemeral=True
            )


        embed = interaction.message.embeds[0]

        embed.color = discord.Color.red()

        embed.add_field(
            name="❌ Решение",
            value=f"Отклонил: {interaction.user.mention}",
            inline=False
        )


        for item in self.children:
            item.disabled = True


        await interaction.message.edit(
            embed=embed,
            view=self
        )


        await interaction.response.send_message(
            "Заявка отклонена.",
            ephemeral=True
        )



    @discord.ui.button(
        label="📋 Создать запрос",
        style=discord.ButtonStyle.primary
    )
    async def new_request(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.send_modal(
            AdminRequestModal()
        )



# ==========================
# ПАНЕЛЬ
# ==========================


@bot.command()
@commands.has_permissions(administrator=True)
async def панель(ctx):

    if ctx.channel.id != REQUEST_CHANNEL_ID:
        return


    embed = discord.Embed(
        title="👑 Запрос административной роли",
        description=(
            "Заполните заявку для получения роли.\n\n"
            "📌 Нужно указать:\n"
            "• Ник\n"
            "• Профиль\n"
            "• Ранг\n"
            "• Период\n"
            "• Скрин с сайта(профиль)\n\n"
            "📸 Скрин загружать через yapx.ru"
        ),
        color=discord.Color.gold()
    )


    await ctx.send(
        embed=embed,
        view=CreateRequest()
    )



@bot.event
async def on_ready():

    print(
        f"Бот запущен: {bot.user}"
    )



bot.run(TOKEN)
