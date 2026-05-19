import discord
import asyncio
import io

class FecharTicketModal(discord.ui.Modal, title="Finalizar Ticket"):

    solucao = discord.ui.TextInput(
        label="Solução do chamado",
        placeholder="Informe como o problema foi resolvido...",
        style=discord.TextStyle.paragraph,
        max_length=1000
    )

    async def on_submit(
        self,
        interaction: discord.Interaction
    ):

        usuario_ticket = None

        # procura usuário do ticket
        for alvo, permissao in interaction.channel.overwrites.items():

            if isinstance(alvo, discord.Member):

                # ignora o bot
                if alvo != interaction.guild.me:

                    usuario_ticket = alvo
                    break

        # responde imediatamente à interaction
        await interaction.response.defer(
            ephemeral=True
        )

        try:

            # cria transcript
            transcript = io.StringIO()

            async for mensagem in interaction.channel.history(
                limit=None,
                oldest_first=True
            ):

                autor = mensagem.author
                conteudo = mensagem.content
                data = mensagem.created_at.strftime(
                    "%d/%m/%Y %H:%M:%S"
                )

                transcript.write(
                    f"[{data}] {autor}: {conteudo}\n"
                )

            # transforma transcript em bytes
            conteudo_transcript = (
                transcript.getvalue().encode()
            )

            # envia DM para usuário
            if usuario_ticket:

                try:

                    embed_dm = discord.Embed(
                        title="🎫 Ticket Finalizado",
                        description=(
                            f"Seu atendimento foi encerrado por "
                            f"{interaction.user.mention}"
                        ),
                        color=discord.Color.red(),
                        timestamp=discord.utils.utcnow()
                    )

                    embed_dm.add_field(
                        name="📝 Solução",
                        value=self.solucao.value,
                        inline=False
                    )

                    embed_dm.set_footer(
                        text=f"Servidor: {interaction.guild.name}"
                    )

                    await usuario_ticket.send(
                        embed=embed_dm,
                        file=discord.File(
                            fp=io.BytesIO(
                                conteudo_transcript
                            ),
                            filename=(
                                f"transcript-"
                                f"{interaction.channel.name}.txt"
                            )
                        )
                    )

                except Exception as e:

                    print(f"[ERRO DM] {e}")

            # mensagem final
            await interaction.followup.send(
                "🔒 Encerrando ticket em 5 segundos...",
                ephemeral=True
            )

            await asyncio.sleep(5)

            await interaction.channel.delete()

        except Exception as e:

            print(f"[ERRO TRANSCRIPT] {e}")

            await interaction.followup.send(
                f"Erro ao fechar ticket: {e}",
                ephemeral=True
            )


class FecharTicketView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)

    @discord.ui.button(
        label="Encerrar Atendimento",
        style=discord.ButtonStyle.red,
        emoji="🔒",
        custom_id="fechar_ticket"
    )
    async def fechar_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        # verifica permissão
        if not interaction.user.guild_permissions.manage_channels:

            await interaction.response.send_message(
                "Você não pode encerrar tickets.",
                ephemeral=True
            )
            return

        # abre modal
        await interaction.response.send_modal(
            FecharTicketModal()
        )