import traceback
from typing import List, Dict, Any, Optional
from database import fetchall, fetchone

def get_recent_images_data(limit: int = 100000) -> List[Dict[str, Any]]:
    """Busca os dados da tabela banco_imagens."""
    try:
        sql = f"""
        SELECT 
            bi.id,
            bi.gaiola,
            bi.tamanho,
            bi.data_captura,
            bi.caminho_arquivo,
            iot.localizacao AS dispositivo_localizacao
        FROM banco_imagens bi
        LEFT JOIN IoT iot ON bi.id_dispositivo = iot.id_dispositivo
        ORDER BY bi.data_captura DESC
        LIMIT %s;
        """
        rows = fetchall(sql, [limit])
        
        def format_bytes(bytes_value):
            if bytes_value is None: return "N/A"
            bytes_value = int(bytes_value)
            if bytes_value < 1024: return f"{bytes_value} B"
            if bytes_value < 1024 * 1024: return f"{bytes_value / 1024:.2f} KB"
            return f"{bytes_value / (1024 * 1024):.2f} MB"

        return [
            {
                "id": row['id'],
                "gaiola": int(row['gaiola']),
                "tamanho": format_bytes(row['tamanho']),
                "data_captura": row['data_captura'].strftime('%Y-%m-%d %H:%M:%S') if row['data_captura'] else "N/A",
                "localizacao": row['dispositivo_localizacao'] if row['dispositivo_localizacao'] else "Desconhecida",
                "nome_arquivo": row['caminho_arquivo'].split('/')[-1] if row['caminho_arquivo'] else "N/A",
            }
            for row in rows
        ]
    except Exception as e:
        print(f"Erro em get_recent_images_data: {e}")
        traceback.print_exc()
        return []

def get_all_images_summary(search_query: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
    """Busca um resumo das imagens mais recentes para o grid do database.html."""
    try:
        search_query = search_query.strip().lower() if search_query else None

        sql_base = f"""
        WITH LastResult AS (
            SELECT
                dr.id_processamento,
                dr.etapa_ciclo,
                dr.quantidade_insetos
            FROM dados_resultado dr
            JOIN dados_ML dm ON dr.id_processamento = dm.id_processamento
        )
        SELECT 
            bi.id AS image_id,
            bi.caminho_arquivo,
            bi.data_captura,
            bi.gaiola,
            (SELECT dr.etapa_ciclo FROM dados_ML dm 
             LEFT JOIN LastResult dr ON dm.id_processamento = dr.id_processamento
             WHERE dm.id_imagem = bi.id
             ORDER BY dm.data_processamento DESC 
             LIMIT 1) AS main_phase,
            (SELECT dr.quantidade_insetos FROM dados_ML dm 
             LEFT JOIN LastResult dr ON dm.id_processamento = dr.id_processamento
             WHERE dm.id_imagem = bi.id
             ORDER BY dm.data_processamento DESC 
             LIMIT 1) AS insect_count,
            (SELECT dr.etapa_ciclo FROM dados_ML dm 
             LEFT JOIN LastResult dr ON dm.id_processamento = dr.id_processamento
             WHERE dm.id_imagem = bi.id
             ORDER BY dm.data_processamento DESC 
             LIMIT 1) AS search_phase
        FROM banco_imagens bi
        """

        where_conditions = []
        params = []

        if search_query:
            print(f"DB: Aplicando filtro de pesquisa: {search_query}")
            where_conditions.append(f"""(
                LOWER(bi.caminho_arquivo) LIKE %s OR 
                LOWER((
                    SELECT dr.etapa_ciclo 
                    FROM dados_ML dm 
                    LEFT JOIN LastResult dr ON dm.id_processamento = dr.id_processamento
                    WHERE dm.id_imagem = bi.id
                    ORDER BY dm.data_processamento DESC 
                    LIMIT 1
                )) LIKE %s
            )""")
            params.append(f"%{search_query}%")
            params.append(f"%{search_query}%")

        if where_conditions:
            sql_base += " WHERE " + " AND ".join(where_conditions)

        sql_base += f" ORDER BY bi.data_captura DESC LIMIT {limit};"

        rows = fetchall(sql_base, params)

        return [
            {
                "id": row['image_id'],
                "file_name": row['caminho_arquivo'].split('/')[-1] if row['caminho_arquivo'] else "N/A",
                "caminho_arquivo": row['caminho_arquivo'],
                "data_captura": row['data_captura'].strftime('%Y-%m-%d %H:%M:%S') if row['data_captura'] else "N/A",
                "gaiola": int(row['gaiola']),
                "fase_principal": row['main_phase'] if row['main_phase'] else "Não Processado",
                "contagem": int(row['insect_count']) if row['insect_count'] is not None else 0,
            }
            for row in rows
        ]
    except Exception as e:
        print(f"Erro em get_all_images_summary: {e}")
        traceback.print_exc()
        return []

def get_image_details(image_id: int) -> Optional[Dict[str, Any]]:
    """Busca todos os detalhes de uma imagem e seu último processamento."""
    try:
        sql = """
        WITH LatestProcessing AS (
            SELECT
                dm.id_imagem,
                MAX(dm.id_processamento) AS latest_id_processamento
            FROM dados_ML dm
            WHERE dm.id_imagem = %s
            GROUP BY dm.id_imagem
        )
        SELECT 
            bi.id AS image_id,
            bi.caminho_arquivo,
            bi.gaiola,
            bi.tamanho,
            bi.data_captura,
            iot.localizacao AS dispositivo_localizacao,
            dm.velocidade_cpu,
            dm.versao_modelo,
            dr.etapa_ciclo,
            dr.quantidade_insetos,
            dr.precisao,
            dr.sexo
        FROM banco_imagens bi
        LEFT JOIN LatestProcessing lp ON bi.id = lp.id_imagem
        LEFT JOIN dados_ML dm ON lp.latest_id_processamento = dm.id_processamento
        LEFT JOIN dados_resultado dr ON dm.id_processamento = dr.id_processamento
        LEFT JOIN IoT iot ON bi.id_dispositivo = iot.id_dispositivo
        WHERE bi.id = %s;
        """
        row = fetchone(sql, [image_id, image_id])

        if not row:
            return None

        data_captura = row['data_captura']
        tamanho_bytes = row['tamanho']

        def format_bytes(bytes_value):
            if bytes_value is None: return "N/A"
            if bytes_value < 1024: return f"{bytes_value} B"
            if bytes_value < 1024 * 1024: return f"{bytes_value / 1024:.2f} KB"
            return f"{bytes_value / (1024 * 1024):.2f} MB"

        return {
            "id": int(row['image_id']),
            "file_name": row['caminho_arquivo'].split('/')[-1] if row['caminho_arquivo'] else "N/A",
            "caminho_arquivo": row['caminho_arquivo'],
            "data": data_captura.strftime('%Y-%m-%d') if data_captura else "N/A",
            "hora": data_captura.strftime('%H:%M:%S') if data_captura else "N/A",
            "gaiola": int(row['gaiola']),
            "tamanho_arquivo": format_bytes(tamanho_bytes),
            "dispositivo": row['dispositivo_localizacao'] if row['dispositivo_localizacao'] else "Dispositivo Desconhecido",
            "fase": row['etapa_ciclo'] if row['etapa_ciclo'] else "Não Processado",
            "quantidade": int(row['quantidade_insetos']) if row['quantidade_insetos'] is not None else 0,
            "precisao": f"{round(float(row['precisao']), 2)}%" if row['precisao'] is not None else "N/A",
            "velocidade_cpu": f"{round(float(row['velocidade_cpu']), 1)} ms" if row['velocidade_cpu'] is not None else "N/A",
            "versao_modelo": row['versao_modelo'] if row['versao_modelo'] else "N/A",
            "sexo_detectado": row['sexo'] if row['sexo'] else "N"
        }

    except Exception as e:
        print(f"Erro em get_image_details: {e}")
        traceback.print_exc()
        return None