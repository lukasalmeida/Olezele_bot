import discord

from views.fechar_ticket_view import FecharTicketView


class TicketView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)

    @discord.ui.button(
        label="Abrir Ticket",
        style=discord.ButtonStyle.green,
        emoji="📩",
        custom_id="abrir_ticket"
    )
    async def abrir_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        try:
            guild = interaction.guild

            # cargo staff
            cargo_staff = guild.get_role(1501227598842171563)

            if cargo_staff is None:

                await interaction.response.send_message(
                    "Cargo staff não encontrado.",
                    ephemeral=True
                )
                return

            # categoria
            categoria = discord.utils.get(
                guild.categories,
                name="「👨‍💻」SUPORTE"
            )

            # cria categoria se não existir
            if categoria is None:

                categoria = await guild.create_category(
                    "「👨‍💻」SUPORTE"
                )

            # evita ticket duplicado
            canal_existente = discord.utils.get(
                guild.text_channels,
                name=f"ticket-{interaction.user.id}"
            )

            if canal_existente:

                await interaction.response.send_message(
                    f"Você já possui um ticket: {canal_existente.mention}",
                    ephemeral=True
                )
                return

            # permissões
            overwrites = {

                # everyone
                guild.default_role: discord.PermissionOverwrite(
                    view_channel=False
                ),

                # usuário que abriu
                interaction.user: discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    attach_files=True,
                    embed_links=True
                ),

                # staff
                cargo_staff: discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    manage_messages=True
                ),

                # bot
                guild.me: discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True
                )
            }

            # cria canal
            canal = await guild.create_text_channel(
                name=f"ticket-{interaction.user.name}",
                category=categoria,
                overwrites=overwrites
            )

            await interaction.response.send_message(
                f"Ticket criado: {canal.mention}",
                ephemeral=True
            )

            embed = discord.Embed(
                title="🎫 Atendimento iniciado",
                description="Descreva seu problema.",
                color=discord.Color.blue()
            )

            view = FecharTicketView()

            await canal.send(
                content=f"{interaction.user.mention} {cargo_staff.mention}",
                embed=embed,
                view=view
            )
        except Exception as e:

            print(f"ERRO NO TICKET: {e}")

            if not interaction.response.is_done():

                await interaction.response.send_message(
                    "Ocorreu um erro ao criar o ticket.",
                    ephemeral=True
                )