import discord
from discord.ext import commands
from discord import app_commands

from views.ticket_view import TicketView


class Tickets(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @app_commands.command(
        name="ticket",
        description="Enviar painel de tickets"
    )
    async def ticket(
        self,
        interaction: discord.Interaction
    ):

        embed = discord.Embed(
            title="🎫 Central de Suporte",
            description=(
                "Clique no botão abaixo para abrir um ticket.\n\n"
                "Nossa equipe responderá assim que possível."
            ),
            color=discord.Color.green()
        )

        embed.set_footer(
            text="Sistema de suporte"
        )

        view = TicketView()

        # envia o painel no canal
        await interaction.channel.send(
            embed=embed,
            view=view
        )

        # responde invisível
        await interaction.response.send_message(
            "Painel enviado com sucesso.",
            ephemeral=True
        )


async def setup(bot):

    await bot.add_cog(Tickets(bot))