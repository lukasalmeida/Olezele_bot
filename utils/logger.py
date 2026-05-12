from database import pegar_log_channel

async def log(bot, guild_id, mensagem=None,embed=None):
        channel_log_id = pegar_log_channel(guild_id)
        if channel_log_id:
            try:
                canal_log = await bot.fetch_channel(channel_log_id)
                await canal_log.send(content=mensagem,embed=embed)
            except Exception as e:
                print(f"[ERRO LOG] {e}")