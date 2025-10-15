import psycopg2
from tqdm import tqdm
from datetime import datetime
import os
import logging
import sys
from dotenv import load_dotenv

load_dotenv()

ORIGEM_CONFIG = {
    "host": os.getenv("ORIGEM_HOST"),
    "dbname": os.getenv("ORIGEM_DBNAME"),
    "user": os.getenv("ORIGEM_USER"),
    "password": os.getenv("ORIGEM_PASSWORD"),
    "port": os.getenv("ORIGEM_PORT")
}

DESTINO_CONFIG = {
    "host": os.getenv("DESTINO_HOST"),
    "dbname": os.getenv("DESTINO_DBNAME"),
    "user": os.getenv("DESTINO_USER"),
    "password": os.getenv("DESTINO_PASSWORD"),
    "port": os.getenv("DESTINO_PORT")
}


with open('query.sql', 'r', encoding='utf-8') as f:
    ORIGINAL_QUERY = f.read()

TABELA_DESTINO = os.getenv("DESTINO_TABLE_NAME")

def executar_migracao():
    try:
        # Conexões
        conn_origem = psycopg2.connect(**ORIGEM_CONFIG)
        cur_origem = conn_origem.cursor()

        conn_destino = psycopg2.connect(**DESTINO_CONFIG)
        cur_destino = conn_destino.cursor()

        # Executa a query de origem
        cur_origem.execute(ORIGINAL_QUERY)
        rows = cur_origem.fetchall()
        colunas = [desc[0] for desc in cur_origem.description if desc[0] != 'id']
        colunas.append("dt_insercao")

        if not rows:
            print("Nenhum dado retornado da consulta.")
            return

        # Adiciona a coluna dt_insercao
        placeholders = ', '.join(['%s'] * len(colunas))
        colunas_str = ', '.join(colunas)
        insert_query = f"""
            INSERT INTO {TABELA_DESTINO} ({colunas_str})
            VALUES ({placeholders});
        """

        for row in tqdm(rows, "Migrando dados"):
            row_com_data = list(row) + [datetime.now()]
            cur_destino.execute(insert_query, row_com_data)

        conn_destino.commit()
        print(f"[{datetime.now()}] Inserção concluída: {len(rows)} registros.")

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        cur_origem.close()
        conn_origem.close()
        cur_destino.close()
        conn_destino.close()


# Base do script (independente de onde o VS Code inicia o processo)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# Caminho ABSOLUTO do log do dia
log_filename = os.path.join(LOGS_DIR, datetime.now().strftime("app_%Y-%m-%d.log"))
print(f"Usando log em: {log_filename}")

def ja_rodou_com_sucesso_hoje(path: str) -> bool:
    if not os.path.isfile(path):
        return False
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            conteudo = f.read()
        return "Script finalizado com sucesso." in conteudo
    except Exception:
        # Se não conseguiu ler, por segurança não bloqueia
        return False

# Só aborta se o log do dia EXISTIR e contiver a mensagem de sucesso
if ja_rodou_com_sucesso_hoje(log_filename):
    print("⚠️ Script já rodou hoje com sucesso. Abortando segunda execução.")
    sys.exit(0)

# Configura logging (append)
logging.basicConfig(
    filename=log_filename,
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Início do script")

try:
    # --- sua lógica principal ---
    executar_migracao()
    logging.info("Rodando lógica principal...")

    # Se chegou aqui, deu tudo certo
    logging.info("Script finalizado com sucesso.")
except Exception as e:
    logging.error(f"Erro durante execução: {e}")
    raise
