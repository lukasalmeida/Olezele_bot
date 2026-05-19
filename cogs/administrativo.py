import discord
from discord.ext import commands
from discord import app_commands

from database.database import salvar_log_channel

class Administrativo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #setlog
    @app_commands.command(name='setlog', description='Seta o canal que armazenará as logs')
    @app_commands.describe(canal="Canal do log")
    async def setlog(self,interaction: discord.Interaction, canal: discord.TextChannel):

        await interaction.response.defer(ephemeral=True)
        if not interaction.user.guild_permissions.administrator:
            await interaction.followup.send(
                "Só admin pode fazer isso.",
                ephemeral=True
            )
            return

        salvar_log_channel(interaction.guild.id,canal.id)

        await interaction.followup.send(
            f"Canal de logs definido como {canal.mention}",
            ephemeral=True
        )


        embed = discord.Embed(
            title="📌 CANAL DE LOG DEFINIDO!",
            colour=discord.Colour.blue(),
            timestamp=discord.utils.utcnow(),
        )
        embed.add_field(
            name="Canal",
            value=f"{canal.mention}",
            inline=False
        )
        embed.add_field(
            name="Definido por",
            value=f"{interaction.user.mention}",
            inline=False
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_author(name=str(interaction.user), icon_url=self.bot.user.display_avatar.url)
        embed.set_footer(
            text=f"Servidor: {interaction.guild.name}"
        )


async def setup(bot):
    await bot.add_cog(Administrativo(bot))