import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
)

cursor = db.cursor()

######################################
## LOGS
######################################
#salva a log
def salvar_log_channel(guild_id, channel_id):

    sql = """
    INSERT INTO guild_config (guild_id, log_channel_id)
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE
    log_channel_id = VALUES(log_channel_id)
    """

    valores = (guild_id, channel_id)

    cursor.execute(sql, valores)
    db.commit()

#Pega a log
def pegar_log_channel(guild_id):

    sql = """SELECT log_channel_id FROM guild_config WHERE guild_id = %s"""

    cursor.execute(sql, (guild_id,))

    resultado = cursor.fetchone()

    return resultado[0] if resultado else None