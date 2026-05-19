import psycopg2
import os

from dotenv import load_dotenv

load_dotenv()


def get_connection():

    return psycopg2.connect(
        os.getenv("DB_URL")
    )


######################################
## LOGS
######################################

# salva a log
def salvar_log_channel(guild_id, channel_id):

    try:

        db = get_connection()
        cursor = db.cursor()

        sql = """
        INSERT INTO guild_config (
            guild_id,
            log_channel_id
        )

        VALUES (%s, %s)

        ON CONFLICT (guild_id)

        DO UPDATE SET
            log_channel_id = EXCLUDED.log_channel_id
        """

        valores = (guild_id, channel_id)

        cursor.execute(sql, valores)

        db.commit()

        cursor.close()
        db.close()

    except Exception as e:

        print(f"Erro ao salvar log: {e}")


# pega a log
def pegar_log_channel(guild_id):

    try:

        db = get_connection()
        cursor = db.cursor()

        sql = """
        SELECT log_channel_id
        FROM guild_config
        WHERE guild_id = %s
        """

        cursor.execute(sql, (guild_id,))

        resultado = cursor.fetchone()

        cursor.close()
        db.close()

        return resultado[0] if resultado else None

    except Exception as e:

        print(f"Erro ao buscar log: {e}")

        return None