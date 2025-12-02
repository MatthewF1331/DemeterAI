import psycopg2
import psycopg2.extras
import os
from datetime import datetime

DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "db"),
    "dbname": os.getenv("POSTGRES_DB", "demeter"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "1234"),
    "port": os.getenv("POSTGRES_PORT", "5432")
}

def get_conn():
    return psycopg2.connect(**DB_CONFIG)

# Retorna o id da imagem com base no nome do arquivo
# Ex: "I001-01-001.jpg" retorna o ID 001 
def get_image_id(filename):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("""
        SELECT id 
        FROM banco_imagens
        WHERE caminho_arquivo = %s
        LIMIT 1
    """, (filename,))

    row = cur.fetchone()
    cur.close()
    conn.close()

    return row["id"] if row else None

# Insere dados na tabela dados_ML e retorna id_processamento
def insert_ml_result(id_imagem, modelo, previsao_media, velocidade_cpu, versao_modelo, parametros):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO dados_ML (
            id_imagem, modelo, previsao_media,
            velocidade_cpu, versao_modelo, parametros
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id_processamento
    """, (id_imagem, modelo, previsao_media, velocidade_cpu, versao_modelo, parametros))

    pid = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()
    return pid

# Insere dados na tabela dados_resultado
def insert_processed_result(id_processamento, sexo, quantidade_insetos, etapa, precisao):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO dados_resultado (
            id_processamento, sexo, quantidade_insetos,
            etapa_ciclo, precisao
        )
        VALUES (%s, %s, %s, %s, %s)
    """, (id_processamento, sexo, quantidade_insetos, etapa, precisao))

    conn.commit()
    cur.close()
    conn.close()

# Retorna o próximo registro da tabela banco_imagens
def get_next_image(last_processed_id):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute("""
        SELECT id, caminho_arquivo 
        FROM banco_imagens
        WHERE id > %s
        ORDER BY id ASC
        LIMIT 1
    """, (last_processed_id,))
    
    row = cur.fetchone()
    cur.close()
    conn.close()
    
    if row:
        return row['id'], row['caminho_arquivo']
    return None, None

# Retorna o último id_imagem processado na tabela dados_ml.
def get_last_processed_image():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT COALESCE(MAX(id_imagem), 0)
        FROM dados_ML
    """)

    last_id = cur.fetchone()[0]

    cur.close()
    conn.close()
    return last_id
