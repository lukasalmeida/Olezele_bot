import os
import threading

import discord
from discord.ext import commands
from dotenv import load_dotenv

from flask import Flask

from utils.logger import log
from views.fechar_ticket_view import FecharTicketView
from views.ticket_view import TicketView

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

app = Flask(__name__)

@app.route("/")
def home():
    return "Olezele Bot Online"


def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


intents = discord.Intents.default()
intents.message_content = True
intents.members = True


class OlezeleBot(commands.Bot):

    async def setup_hook(self):

        # cogs
        await self.load_extension("cogs.administrativo")
        await self.load_extension("cogs.moderacao")
        await self.load_extension("cogs.utilidades")
        await self.load_extension("cogs.tickets")

        # views persistentes
        self.add_view(TicketView())
        self.add_view(FecharTicketView())

        # sync slash commands
        synced = await self.tree.sync()

        print(f"Sincronizados: {len(synced)} comandos")


bot = OlezeleBot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():

    print(f"Bot online como {bot.user}")

    embed = discord.Embed(
        title="🟢 Bot online",
        description=f"Bot online como {bot.user}",
        color=discord.Color.green(),
        timestamp=discord.utils.utcnow(),
    )

    for guild in bot.guilds:
        try:
            await log(bot, guild.id, embed=embed)
        except Exception as e:
            print(f"Erro ao enviar log: {e}")


# ===================================
# START
# ===================================

threading.Thread(target=run_web).start()

bot.run(TOKEN)