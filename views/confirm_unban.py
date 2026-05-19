import discord

from utils.logger import log


class ConfirmUnban(discord.ui.View):

    def __init__(self, bot, usuario, moderador, motivo):

        super().__init__(timeout=60)

        self.bot = bot
        self.usuario = usuario
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
            await interaction.guild.unban(self.usuario, reason=self.motivo)

            #resposta comando
            embed = discord.Embed(
                title="🟢 USUÁRIO DESBANIDO!",
                colour=discord.Colour.red(),
                timestamp=discord.utils.utcnow(),
            )

            embed.add_field(
                name="Usuário",
                value=f"<@{self.usuario.id}>",
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
                content=f"{self.usuario.mention} foi desbanido!",
                view=None
            )

            #log
            embed = discord.Embed(
                title="🟢 USUÁRIO DESBANIDO!",
                colour=discord.Colour.green(),
                timestamp=discord.utils.utcnow(),
            )
            embed.add_field(
                name="Usuário",
                value=f"{self.usuario.mention}",
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
            content="Unban cancelado",
            view=None
        )
