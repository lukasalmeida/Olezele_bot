import discord

from utils.logger import log


class ConfirmLimpar(discord.ui.View):

    def __init__(self, bot, quantidade, canal, moderador):

        super().__init__(timeout=60)

        self.bot = bot
        self.quantidade = quantidade
        self.canal = canal
        self.moderador = moderador

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
            mensagem_confirmacao = interaction.message

            await interaction.response.edit_message(
                content=f"✅ {self.quantidade} mensagens limpas!",
                view=None
            )

            mensagens = await interaction.channel.purge(
                limit=self.quantidade,
                check=lambda m: m.id != mensagem_confirmacao.id
            )


            embed = discord.Embed(
                title="▶️ COMANDO EXECUTADO!",
                colour=discord.Colour.green(),
                timestamp=discord.utils.utcnow(),
            )
            embed.add_field(
                name="Comando",
                value="/limpar",
                inline=False
            )
            embed.add_field(
                name="Aba",
                value=f"{interaction.channel.mention}",
                inline=False
            )
            embed.add_field(
                name="Quantidade",
                value=f"{len(mensagens)}",
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
                f"Erro ao limpar: {e}",
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
            content="Limpeza cancelado",
            view=None
        )
