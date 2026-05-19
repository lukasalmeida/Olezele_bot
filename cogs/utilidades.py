import discord
from discord.ext import commands
from discord import app_commands

from views.confirm_limpar import ConfirmLimpar
from models.anuncio_modal import AnuncioModal

class Utilidades(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #ping
    @app_commands.command(
        name="ping",
        description="Testa o bot e exibe a latência",
    )
    async def ping(self,interaction: discord.Interaction):
        await  interaction.response.defer(ephemeral=True)
        await interaction.followup.send(f'🏓 Pong! {round(self.bot.latency * 1000)}ms', ephemeral=True)

        embed = discord.Embed(
            title="▶️ COMANDO EXECUTADO!",
            colour=discord.Colour.green(),
            timestamp=discord.utils.utcnow(),
        )
        embed.add_field(
            name="Comando",
            value="/ping",
            inline=False
        )
        embed.add_field(
            name="Latência",
            value=f"{round(self.bot.latency * 1000)}ms",
            inline=False
        )
        embed.add_field(
            name="Aba",
            value=f"{interaction.channel.mention}",
            inline=False
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_author(name=str(interaction.user), icon_url=self.bot.user.display_avatar.url)
        embed.set_footer(
            text=f"Servidor: {interaction.guild.name}"
        )

    #Limpa chat
    @app_commands.command(name="limpar", description='Limpa o chat')
    @app_commands.describe(quantidade="Quantidde de mensagens a apagar")
    async def limpar(self,interaction: discord.Interaction, quantidade: int):
        await interaction.response.defer(ephemeral=True)
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.followup.send("Sem permissão guerreiro", ephemeral=True)
            return
        try:
            view = ConfirmLimpar(
                self.bot,
                quantidade,
                interaction.channel,
                interaction.user
            )
            await interaction.followup.send(
                f"Você deseja realmente limpar {quantidade} mensagens em {interaction.channel.mention}?",
                view=view,
                ephemeral=True
            )

        except Exception as e:
            await interaction.followup.send(f"Erro ao limpar : {e}")

    #Anuncio
    @app_commands.command(
        name="anuncio",
        description="Criar um anúncio"
    )
    async def anuncio(self,interaction: discord.Interaction):
        modal = AnuncioModal()

        await interaction.response.send_modal(modal)

async def setup(bot):
    await bot.add_cog(Utilidades(bot))