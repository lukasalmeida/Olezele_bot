import discord
from discord.ext import commands
from discord import app_commands

from utils.logger import log
from views import confirm_ban
from views.confirm_ban import ConfirmBan
from views.confirm_unban import ConfirmUnban

class Moderacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #ban
    @app_commands.command(
        name="ban",
        description="Banir usuário do servidor"
    )
    async def ban(self, interaction: discord.Interaction,membro: discord.Member,motivo: str = "Sem motivo"):
        #Sem permissão
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message(
                "Você não tem permissão para banir.",
                ephemeral=True
            )
            return

        #Não pode banir a si mesmo
        if membro == interaction.user:
            await interaction.response.send_message(
                "Você não pode se banir.",
                ephemeral=True
            )
            return

        #Não pode banir o dono
        if membro == interaction.guild.owner:
            await interaction.response.send_message(
                "Você não pode banir o dono do servidor.",
                ephemeral=True
            )
            return

        #Hierarquia de cargos (usuário)
        if membro.top_role >= interaction.user.top_role:
            await interaction.response.send_message(
                "Você não pode banir alguém com o cargo maior que o seu.",
                ephemeral=True
            )
            return

        #Hierarquia de cargos (bot)
        if membro.top_role >= interaction.guild.me.top_role:
            await interaction.response.send_message(
                "Eu não posso banir esse usuário (cargo maior que o meu)",
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)

        try:
            view = ConfirmBan(
                self.bot,
                membro,
                interaction.user,
                motivo
            )
            await interaction.followup.send(
                f"Você deseja realmente banir {membro.mention}?",
                view=view,
                ephemeral=True
            )

        except Exception as e:
            await interaction.followup.send(f"Erro ao banir : {e}")

    #Unban
    @app_commands.command(name='unban', description='Desbanir usuários do servidor')
    @app_commands.describe(user_id="ID do usuário", motivo="motivo do desbanimento")
    async def unban(self,interaction: discord.Interaction,user_id: str, motivo: str  = "Sem motivo"):
        #permissão
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message(
                f"Você não tem permissão para desbanir"
            )
            return

        await interaction.response.defer(ephemeral=True)

        try:
            #Busca o usuário por API
            usuario = await self.bot.fetch_user(int(user_id))

            #remove ban
            #await interaction.guild.unban(usuario, reason=motivo)
            view = ConfirmUnban(
                self.bot,
                usuario,
                interaction.user,
                motivo
            )
            await interaction.followup.send(
                f"Você deseja realmente desbanir <@{usuario.id}> ?",
                view=view,
                ephemeral=True
            )

        except Exception as e:
            await interaction.followup.send(f"Erro ao desbanir : {e}")



async def setup(bot):
    await bot.add_cog(Moderacao(bot))