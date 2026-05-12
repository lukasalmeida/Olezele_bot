import discord

from utils.logger import log


class ConfirmBan(discord.ui.View):

    def __init__(self, bot, membro, moderador, motivo):

        super().__init__(timeout=60)

        self.bot = bot
        self.membro = membro
        self.moderador = moderador
        self.motivo = motivo

    # confirmar
    @discord.ui.button(
        label="Confirmar",
        style=discord.ButtonStyle.green,
        emoji="✅"
    )
    async def confirmar(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):

        if interaction.user != self.moderador:
            await interaction.response.send_message(
                "Você não pode usar este botão",
                ephemeral=True
            )
            return

        try:
            await self.membro.ban(reason=self.motivo)

            #resposta comando
            embed = discord.Embed(
                title="⛔ USUÁRIO BANIDO!",
                colour=discord.Colour.red(),
                timestamp=discord.utils.utcnow(),
            )

            embed.add_field(
                name="Usuário",
                value=f"{self.membro.mention} ({self.membro.id})",
                inline=False
            )

            embed.add_field(
                name="Motivo",
                value=f"{self.motivo}",
                inline=False
            )

            embed.add_field(
                name="Administrador",
                value=f"{interaction.user.mention}",
                inline=False
            )

            embed.set_thumbnail(url=self.bot.user.display_avatar.url)

            embed.set_author(
                name=str(interaction.user),
                icon_url=self.bot.user.display_avatar.url
            )

            embed.set_footer(
                text=f"Servidor: {interaction.guild.name}"
            )

            await log(self.bot, interaction.guild.id, embed=embed)

            await interaction.response.edit_message(
                content=f"{self.membro.mention} ({self.membro.id}) foi banido!",
                view=None
            )

            #log
            embed = discord.Embed(
                title="⛔ USUÁRIO BANIDO!",
                colour=discord.Colour.red(),
                timestamp=discord.utils.utcnow(),
            )
            embed.add_field(
                name="Usuário",
                value=f"{self.membro.mention} ({self.membro.id})",
                inline=False
            )
            embed.add_field(
                name="Motivo",
                value=f"{self.motivo}",
                inline=False
            )
            embed.add_field(
                name="Administrador",
                value=f"{interaction.user.mention}",
                inline=False
            )
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            embed.set_author(name=str(interaction.user), icon_url=self.bot.user.display_avatar.url)
            embed.set_footer(
                text=f"Servidor: {interaction.guild.name}"
            )

            await log(self.bot,interaction.guild.id,embed=embed)

        except Exception as e:
            await interaction.followup.send(
                f"Erro ao banir: {e}",
                ephemeral=True
            )

    # cancelar
    @discord.ui.button(
        label="Cancelar",
        style=discord.ButtonStyle.secondary,
        emoji="❌"
    )
    async def cancelar(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):

        if interaction.user != self.moderador:
            await interaction.response.send_message(
                "Você não pode usar este botão",
                ephemeral=True
            )
            return

        await interaction.response.edit_message(
            content="Ban cancelado",
            view=None
        )
