import discord
from discord import emoji
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

from utils.logger import log
from views.fechar_ticket_view import FecharTicketView

from views.ticket_view import TicketView

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GG = os.getenv('GUILD')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
guild = discord.Object(id=int(GG))

@bot.event
async def on_ready():
    bot.add_view(TicketView())
    bot.add_view(FecharTicketView())
    
    synced = await bot.tree.sync()
    print(f"Sincronizados: {len(synced)} comandos")


    print(f"Bot online como {bot.user}")

    embed = discord.Embed(
        title="🟢 Bot online",
        description=f"Bot online como {bot.user}",
        color=discord.Color.green(),
        timestamp=discord.utils.utcnow(),
    )

    await log(bot,guild.id, embed=embed)


async def main():
    async with bot:

        await bot.load_extension("cogs.administrativo")
        await bot.load_extension("cogs.moderacao")
        await bot.load_extension("cogs.utilidades")
        await bot.load_extension("cogs.tickets")

        await bot.start(TOKEN)

asyncio.run(main())