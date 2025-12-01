import psycopg2
from psycopg2.extras import RealDictCursor
import traceback
from typing import List, Optional, Dict, Any
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

# Cria e retorna uma conexão com o PostgreSQL
def get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )

# Executa SELECT e retorna um único resultado como dicionário (fetch ONE)
def fetchone(sql: str, params: Optional[List[Any]] = None) -> Optional[Dict[str, Any]]:
    params = params or []
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql, params)
        row = cur.fetchone()
        cur.close()
        return row
    except Exception as e:
        print(f"Erro em fetchone (DB ERROR): {e}")
        traceback.print_exc()
        return None
    finally:
        if conn:
            conn.close()

# Executa SELECT e retorna todos os resultados como lista de dicionários (fetch ALL)
def fetchall(sql: str, params: Optional[List[Any]] = None) -> List[Dict[str, Any]]:
    params = params or []
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql, params)
        rows = cur.fetchall()
        cur.close()
        return rows
    except Exception as e:
        print(f"Erro em fetchall (DB ERROR): {e}")
        traceback.print_exc()
        return []
    finally:
        if conn:
            conn.close()

# Adiciona a cláusula WHERE para filtrar por data (Auxiliar para queries)
def add_time_filter(sql: str, time_filter: str) -> str:
    if "dm.data_processamento" in sql.lower():
        date_field = "dm.data_processamento"
    elif "bi.data_captura" in sql.lower():
        date_field = "bi.data_captura"
    else:
        return sql

    if "where" in sql.lower():
        last_clause = sql.strip().split()[-1].lower()
        if last_clause == 'where' or last_clause == 'and':
            return f"{sql} {date_field} >= NOW() - INTERVAL '{time_filter}';"
        else:
            return f"{sql} AND {date_field} >= NOW() - INTERVAL '{time_filter}';"
    else:
        return f"{sql} WHERE {date_field} >= NOW() - INTERVAL '{time_filter}';"