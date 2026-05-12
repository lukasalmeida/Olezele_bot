import discord

class AnuncioModal(discord.ui.Modal, title="Criar Anuncio"):

    titulo = discord.ui.TextInput(
        label="Titulo",
        placeholder="Digite o titulo",
        max_length=100
    )
    mensagem = discord.ui.TextInput(
        label="Mensagem",
        style=discord.TextStyle.paragraph,
        placeholder="Digite a mensagem",
        max_length=4000
    )
    imagem = discord.ui.TextInput(
        label="URL da imagem",
        required=False,
        placeholder="Digite o url da imagem",
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=self.titulo.value,
            description=self.mensagem.value,
            colour=discord.Colour.orange(),
            timestamp=discord.utils.utcnow()
        )
        if self.imagem.value:
            embed.set_image(url=self.imagem.value)

        embed.set_author(
            name=str(interaction.user),
            icon_url=interaction.user.display_avatar.url
        )

        await interaction.response.send_message(
            embed=embed
        )