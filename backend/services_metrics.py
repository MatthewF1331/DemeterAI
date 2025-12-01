import traceback
from typing import List, Dict, Any
from collections import defaultdict
from datetime import date
from database import fetchall, fetchone, add_time_filter

# --- MÉTRICAS (M1 até M13) ---

# Total de adultos por gaiola com filtro de tempo (M1)
def get_m1_quantidade_adultos_total(time_filter: str) -> Dict[str, Any]:
    try:
        sql = """
        SELECT 
            COALESCE(SUM(dr.quantidade_insetos), 0) AS total_adultos,
            COUNT(DISTINCT bi.gaiola) AS total_gaiolas
        FROM dados_resultado dr
        JOIN dados_ML dm ON dr.id_processamento = dm.id_processamento
        JOIN banco_imagens bi ON dm.id_imagem = bi.id
        WHERE LOWER(TRIM(dr.etapa_ciclo)) = 'adulto'
        """
        sql_filtered = add_time_filter(sql, time_filter)

        row = fetchone(sql_filtered)
        total_adults = int(row['total_adultos']) if row and row['total_adultos'] else 0
        total_gaiolas = int(row['total_gaiolas']) if row and row['total_gaiolas'] else 0

        return {"valor": total_adults, "gaiolas": total_gaiolas, "unidade": "adultos"}
    except Exception as e:
        print(f"Erro em get_m1_quantidade_adultos_total: {e}")
        traceback.print_exc()
        return {"valor": 0, "gaiolas": 0, "unidade": "adultos"}

# Distribuição total de insetos por fase de vida (M2)
def get_m2_distribuicao_ciclo_vida() -> Dict[str, Any]:
    try:
        sql = """
        SELECT 
            LOWER(TRIM(dr.etapa_ciclo)) as etapa,
            COALESCE(SUM(dr.quantidade_insetos), 0) as total
        FROM dados_resultado dr
        GROUP BY 1;
        """
        rows = fetchall(sql)

        etapas_data = defaultdict(int)
        total_geral = 0
        for row in rows:
            etapa = row['etapa']
            quantidade = int(row['total'])
            etapas_data[etapa] = quantidade
            total_geral += quantidade

        labels = ["Ovo", "Larva", "Pupa", "Adulto"]
        data = [
            etapas_data['ovo'],
            etapas_data['larva'],
            etapas_data['pupa'],
            etapas_data['adulto']
        ]

        return {"labels": labels, "data": data, "total_geral": total_geral}
    except Exception as e:
        print(f"Erro em get_m2_distribuicao_ciclo_vida: {e}")
        traceback.print_exc()
        return {"labels": ["Ovo", "Larva", "Pupa", "Adulto"], "data": [0, 0, 0, 0], "total_geral": 0}

# Taxa de Mortalidade Diária (M3)
def get_m3_taxa_mortalidade_diaria(time_filter: str) -> Dict[str, Any]:
    try:
        if time_filter == "1 day": date_filter = "CURRENT_DATE"
        else: date_filter = f"NOW() - INTERVAL '{time_filter}'"
        
        daily_adults_sql = f"""
        WITH DailyAdults AS (
            SELECT
                DATE(data_captura) AS data_captura_dia,
                bi.gaiola,
                SUM(dr.quantidade_insetos) AS adultos_dia_atual
            FROM dados_resultado dr
            JOIN dados_ML dm ON dr.id_processamento = dm.id_processamento
            JOIN banco_imagens bi ON dm.id_imagem = bi.id
            WHERE LOWER(TRIM(dr.etapa_ciclo)) = 'adulto'
              AND bi.data_captura >= {date_filter}
            GROUP BY 1, 2
        )
        SELECT data_captura_dia, gaiola, adultos_dia_atual
        FROM DailyAdults ORDER BY data_captura_dia;
        """
        rows = fetchall(daily_adults_sql)

        data_by_cage = defaultdict(list)
        for row in rows:
            data_by_cage[row['gaiola']].append(row)

        daily_rates = defaultdict(lambda: {'total_rate': 0.0, 'count': 0})

        for cage, daily_data in data_by_cage.items():
            previous_adults = 0
            for row in daily_data:
                current_adults = int(row['adultos_dia_atual'])
                day = row['data_captura_dia'].strftime('%d/%m')
                if previous_adults > 0:
                    mortalidade = ((previous_adults - current_adults) / previous_adults) * 100
                    rate = max(0.0, min(100.0, round(mortalidade, 2)))
                    daily_rates[day]['total_rate'] += rate
                    daily_rates[day]['count'] += 1
                previous_adults = current_adults

        labels = []
        data = []
        for day, metrics in sorted(daily_rates.items()):
            labels.append(day)
            avg_rate = round(metrics['total_rate'] / metrics['count'], 2)
            data.append(avg_rate)

        global_avg = sum(data) / len(data) if data else 0.0

        return {"labels": labels, "data": data, "kpi_valor": round(global_avg, 2)}
    except Exception as e:
        print(f"Erro em get_m3_taxa_mortalidade_diaria: {e}")
        traceback.print_exc()
        return {"labels": [], "data": [], "kpi_valor": 0.0}

# Área de Necessidade de Intervenção (M4)
def get_m4_necessidade_intervencao_area(time_filter: str) -> Dict[str, Any]:
    try:
        AREA_IDEAL_POR_ADULTO = 0.15
        AREA_TOTAL_GAIOLA = 100

        sql = f"""
        WITH FilteredAdults AS (
            SELECT
                bi.data_captura,
                bi.gaiola,
                dr.quantidade_insetos AS adults_count
            FROM dados_resultado dr
            JOIN dados_ML dm ON dr.id_processamento = dm.id_processamento
            JOIN banco_imagens bi ON dm.id_imagem = bi.id
            WHERE LOWER(TRIM(dr.etapa_ciclo)) = 'adulto'
              AND bi.data_captura >= NOW() - INTERVAL '{time_filter}'
        ),
        WeeklyAdults AS (
            SELECT
                DATE_TRUNC('week', data_captura)::date AS semana,
                SUM(adults_count) AS total_adultos_semanal
            FROM FilteredAdults
            GROUP BY 1
            ORDER BY semana ASC
        )
        SELECT * FROM WeeklyAdults;
        """
        rows = fetchall(sql)
        labels, area_necessaria, area_referencia = [], [], []

        for row in rows:
            semana_dt: date = row['semana']
            total_adultos = int(row['total_adultos_semanal'])
            calc_area = round(total_adultos * AREA_IDEAL_POR_ADULTO, 2)
            labels.append(f"{semana_dt.strftime('%d/%m')}")
            area_necessaria.append(calc_area)
            area_referencia.append(AREA_TOTAL_GAIOLA)

        kpi_valor = 0.0
        if area_necessaria and area_referencia:
            ratios = [a / r for a, r in zip(area_necessaria, area_referencia) if r > 0]
            kpi_valor = round((sum(ratios) / len(ratios)) * 100, 1) if ratios else 0.0

        return {"labels": labels, "area_necessaria": area_necessaria, "area_referencia": area_referencia, "kpi_valor": kpi_valor}
    except Exception as e:
        print(f"Erro em get_m4_necessidade_intervencao_area: {e}")
        traceback.print_exc()
        return {"labels": [], "area_necessaria": [], "area_referencia": [], "kpi_valor": 0.0}

# Média de Captura de Imagens por Dia (M5)
def get_m5_taxa_captura_imagens_diaria(time_filter: str) -> Dict[str, Any]:
    try:
        if time_filter == "1 day": date_filter = "CURRENT_DATE"
        else: date_filter = f"NOW() - INTERVAL '{time_filter}'"
        
        sql = f"""
        SELECT
            DATE(data_captura) AS capture_date,
            COUNT(id) AS total_imagens_dia
        FROM banco_imagens
        WHERE data_captura >= {date_filter}
        GROUP BY 1 ORDER BY 1 DESC LIMIT 7;
        """
        rows = fetchall(sql)
        rows.reverse()

        labels = [row['capture_date'].strftime('%d/%m') for row in rows]
        data = [int(row['total_imagens_dia']) for row in rows]
        kpi_valor = round(sum(data) / len(data)) if data else 0

        return {"labels": labels, "data": data, "kpi_valor": kpi_valor}
    except Exception as e:
        print(f"Erro em get_m5_taxa_captura_imagens_diaria: {e}")
        traceback.print_exc()
        return {"labels": [], "data": [], "kpi_valor": 0}

# Média Diária de Ovos (M6)
def get_m6_quantidade_ovos_diario(time_filter: str) -> Dict[str, Any]:
    try:
        if time_filter == "1 day": date_filter = "CURRENT_DATE"
        else: date_filter = f"NOW() - INTERVAL '{time_filter}'"
        
        sql = f"""
        WITH DailyCounts AS (
            SELECT
                DATE(dm.data_processamento) AS data_dia,
                bi.gaiola,
                COALESCE(SUM(dr.quantidade_insetos), 0) AS daily_insect_count
            FROM dados_resultado dr
            JOIN dados_ML dm ON dr.id_processamento = dm.id_processamento
            JOIN banco_imagens bi ON dm.id_imagem = bi.id
            WHERE LOWER(TRIM(dr.etapa_ciclo)) = 'ovo'
              AND dm.data_processamento >= {date_filter}
            GROUP BY 1, 2
        ),
        AvgDailyCounts AS (
            SELECT
                data_dia,
                ROUND(AVG(daily_insect_count)) AS avg_daily_ovos
            FROM DailyCounts
            GROUP BY 1
            ORDER BY 1 ASC
        )
        SELECT 
            (SELECT ROUND(AVG(avg_daily_ovos)) FROM AvgDailyCounts) AS avg_ovos_total,
            (SELECT COUNT(DISTINCT gaiola) FROM DailyCounts) AS total_gaiolas,
            (SELECT ARRAY_AGG(data_dia::text ORDER BY data_dia) FROM AvgDailyCounts) AS labels_raw,
            (SELECT ARRAY_AGG(avg_daily_ovos ORDER BY data_dia) FROM AvgDailyCounts) AS data
        ;
        """
        row = fetchone(sql)
        if not row: return {"valor": 0, "gaiolas": 0, "unidade": "ovos/dia", "labels": [], "data": []}

        avg_ovos = int(row['avg_ovos_total']) if row['avg_ovos_total'] is not None else 0
        total_gaiolas = int(row['total_gaiolas']) if row['total_gaiolas'] is not None else 0
        labels = [date.fromisoformat(d).strftime('%d/%m') for d in row['labels_raw']] if row['labels_raw'] else []
        data = [int(d) for d in row['data']] if row['data'] else []

        return {"valor": avg_ovos, "gaiolas": total_gaiolas, "unidade": "ovos/dia", "labels": labels, "data": data}
    except Exception as e:
        print(f"Erro em get_m6_quantidade_ovos_diario: {e}")
        traceback.print_exc()
        return {"valor": 0, "gaiolas": 0, "unidade": "ovos/dia", "labels": [], "data": []}

# Taxa diária de ovos depositados por adulto vivo (M7)
def get_m7_taxa_ovop_por_adulto(time_filter: str) -> Dict[str, Any]:
    try:
        if time_filter == "1 day": date_filter = "CURRENT_DATE"
        else: date_filter = f"NOW() - INTERVAL '{time_filter}'"
        
        sql = f"""
        WITH DailyCounts AS (
            SELECT
                DATE(dm.data_processamento) AS data_dia,
                bi.gaiola,
                SUM(CASE WHEN LOWER(TRIM(dr.etapa_ciclo)) = 'ovo' THEN dr.quantidade_insetos ELSE 0 END) AS total_ovos_dia,
                SUM(CASE WHEN LOWER(TRIM(dr.etapa_ciclo)) = 'adulto' THEN dr.quantidade_insetos ELSE 0 END) AS total_adultos_dia
            FROM dados_resultado dr
            JOIN dados_ML dm ON dr.id_processamento = dm.id_processamento
            JOIN banco_imagens bi ON dm.id_imagem = bi.id
            WHERE dm.data_processamento >= {date_filter}
            GROUP BY 1, 2
        ),
        DailyRatios AS (
            SELECT
                data_dia,
                CASE WHEN total_adultos_dia > 0 THEN ROUND(CAST(total_ovos_dia AS NUMERIC) / total_adultos_dia, 2) ELSE 0.0 END AS ovos_por_adulto
            FROM DailyCounts
        )
        SELECT data_dia, ROUND(AVG(ovos_por_adulto), 2) AS media_ovos_por_adulto
        FROM DailyRatios GROUP BY data_dia ORDER BY data_dia ASC;
        """
        rows = fetchall(sql)
        labels, data = [], []

        for row in rows:
            labels.append(row['data_dia'].strftime('%d/%m'))
            data.append(float(row['media_ovos_por_adulto']))

        kpi_valor = sum(data) / len(data) if data else 0.0
        return {"labels": labels, "data": data, "kpi_valor": round(kpi_valor, 2)}
    except Exception as e:
        print(f"Erro em get_m7_taxa_ovop_por_adulto: {e}")
        traceback.print_exc()
        return {"labels": [], "data": [], "kpi_valor": 0.0}

# Taxa de Crescimento diária de adultos (M8)
def get_m8_taxa_crescimento_diaria(time_filter: str) -> Dict[str, Any]:
    try:
        if time_filter == "1 day": date_filter = "CURRENT_DATE"
        else: date_filter = f"NOW() - INTERVAL '{time_filter}'"
        
        sql = f"""
        WITH DailyAdults AS (
            SELECT
                DATE(bi.data_captura) AS data_dia,
                bi.gaiola,
                COALESCE(SUM(dr.quantidade_insetos), 0) AS daily_adult_population
            FROM dados_resultado dr
            JOIN dados_ML dm ON dr.id_processamento = dm.id_processamento
            JOIN banco_imagens bi ON dm.id_imagem = bi.id
            WHERE LOWER(TRIM(dr.etapa_ciclo)) = 'adulto' AND bi.data_captura >= {date_filter}
            GROUP BY 1, 2 ORDER BY data_dia, gaiola
        ),
        GrowthRateRaw AS (
            SELECT
                data_dia, gaiola, daily_adult_population,
                LAG(daily_adult_population, 1, 0) OVER (PARTITION BY gaiola ORDER BY data_dia) AS previous_day_population
            FROM DailyAdults
        )
        SELECT data_dia, gaiola, daily_adult_population,
            CASE WHEN previous_day_population = 0 THEN 0.0
                ELSE ROUND(CAST((daily_adult_population - previous_day_population) AS NUMERIC) * 100.0 / previous_day_population, 2)
            END AS growth_rate_percent
        FROM GrowthRateRaw
        WHERE previous_day_population > 0 OR daily_adult_population > 0 
        ORDER BY data_dia, gaiola;
        """
        rows = fetchall(sql)
        data_by_cage = defaultdict(lambda: {'labels': [], 'data': [], 'adult_count': []})
        all_cages = set()

        for row in rows:
            day = row['data_dia'].strftime('%d/%m')
            gaiola_id = int(row['gaiola'])
            all_cages.add(gaiola_id)
            taxa = float(row['growth_rate_percent'])
            adults = int(row['daily_adult_population'])
            data_by_cage[gaiola_id]['labels'].append(day)
            data_by_cage[gaiola_id]['data'].append(taxa)
            data_by_cage[gaiola_id]['adult_count'].append(adults)

        return {"cages": sorted(list(all_cages)), "data_map": dict(data_by_cage)}
    except Exception as e:
        print(f"Erro em get_m8_taxa_crescimento_diaria: {e}")
        traceback.print_exc()
        return {"cages": [], "data_map": {}}

# Média de Velocidade da cpu/ms (M9)
def get_m9_velocidade_cpu(time_filter: str) -> Dict[str, Any]:
    try:
        sql = "SELECT COALESCE(AVG(velocidade_cpu), 0.0) AS avg_cpu_speed FROM dados_ML WHERE velocidade_cpu IS NOT NULL"
        sql_filtered = add_time_filter(sql, time_filter)
        row = fetchone(sql_filtered)
        avg_speed = float(row['avg_cpu_speed']) if row and row['avg_cpu_speed'] else 0.0
        return {"valor": round(avg_speed, 1), "unidade": "ms"}
    except Exception as e:
        print(f"Erro em get_m9_velocidade_cpu: {e}")
        return {"valor": 0.0, "unidade": "ms"}

# Quantidade de imagens no database (M10)
def get_m10_quantidade_fotos_db(time_filter: str) -> Dict[str, Any]:
    try:
        sql = "SELECT COUNT(id) AS total_fotos FROM banco_imagens"
        sql_filtered = add_time_filter(sql, time_filter)
        row = fetchone(sql_filtered)
        total_fotos = int(row['total_fotos']) if row and row['total_fotos'] else 0
        return {"valor": total_fotos, "unidade": "fotos"}
    except Exception as e:
        print(f"Erro em get_m10_quantidade_fotos_db: {e}")
        return {"valor": 0, "unidade": "fotos"}

# Histórico de porcentagem de precisão por dia (M11)
def get_m11_precisao_diaria_chart(time_filter: str) -> Dict[str, Any]:
    try:
        if time_filter == "1 day": date_filter = "CURRENT_DATE"
        else: date_filter = f"NOW() - INTERVAL '{time_filter}'"
        
        sql = f"""
        SELECT 
            DATE(dm.data_processamento) AS data_dia,
            COALESCE(AVG(dr.precisao), 0.0) AS avg_precision_dia
        FROM dados_resultado dr
        JOIN dados_ML dm ON dr.id_processamento = dm.id_processamento
        WHERE dm.data_processamento >= {date_filter}
        GROUP BY 1 ORDER BY 1 ASC;
        """
        rows = fetchall(sql)
        labels = [row['data_dia'].strftime('%d/%m') for row in rows]
        data = [round(float(row['avg_precision_dia']), 2) for row in rows]
        kpi_valor = sum(data) / len(data) if data else 0.0

        return {"labels": labels, "data": data, "kpi_valor": round(kpi_valor, 2)}
    except Exception as e:
        print(f"Erro em get_m11_precisao_diaria_chart: {e}")
        traceback.print_exc()
        return {"labels": [], "data": [], "kpi_valor": 0.0}

# Média de Captura de Imagens por Dia (M12)
def get_m12_taxa_captura_analise(time_filter: str) -> Dict[str, Any]:
    m5_data = get_m5_taxa_captura_imagens_diaria(time_filter)
    return {"valor": m5_data['kpi_valor'], "unidade": "fotos/dia"}

# Reinoculação dos ovos (M13)
def get_m13_reinocular_ovos(time_filter: str) -> Dict[str, Any]:
    try:
        OVOS_POR_0_4ML = 1000
        DIAS_RELEVANTES = 17
        sql = f"""
        SELECT COALESCE(SUM(dr.quantidade_insetos), 0) AS total_ovos_coletados
        FROM dados_resultado dr
        JOIN dados_ML dm ON dr.id_processamento = dm.id_processamento
        JOIN banco_imagens bi ON dm.id_imagem = bi.id
        WHERE LOWER(TRIM(dr.etapa_ciclo)) = 'ovo'
          AND bi.data_captura >= NOW() - INTERVAL '{DIAS_RELEVANTES} days';
        """
        row = fetchone(sql)
        total_ovos = int(row['total_ovos_coletados']) if row and row['total_ovos_coletados'] else 0
        volume_estimado_ml = round((total_ovos / OVOS_POR_0_4ML) * 0.4, 2)
        target_volume_ml = 0.4
        
        status = "CRÍTICO"
        if volume_estimado_ml >= target_volume_ml * 1.5: status = "EXCELENTE"
        elif volume_estimado_ml >= target_volume_ml: status = "IDEAL"
        elif volume_estimado_ml >= target_volume_ml * 0.75: status = "ATENÇÃO"

        return {
            "total_ovos_17dias": total_ovos,
            "volume_estimado_ml": volume_estimado_ml,
            "volume_target_ml": target_volume_ml,
            "status": status,
            "unidade": "ml"
        }
    except Exception as e:
        print(f"Erro em get_m13_reinocular_ovos: {e}")
        traceback.print_exc()
        return {"total_ovos_17dias": 0, "volume_estimado_ml": 0.0, "volume_target_ml": 0.4, "status": "CRÍTICO", "unidade": "ml"}

# Busca um snapshot dos dados de processamento mais recente
def get_performance_data_latest() -> Dict[str, Any]:
    try:
        latest_proc_sql = "SELECT id_processamento FROM dados_ML ORDER BY data_processamento DESC LIMIT 1;"
        latest_proc_row = fetchone(latest_proc_sql)
        latest_proc_id = latest_proc_row['id_processamento'] if latest_proc_row else 0

        if latest_proc_id == 0:
            return {"modelo": "N/A", "fotos_dia": 0, "precisao_media_latest": "N/A", "velocidade_cpu_latest": "N/A"}

        data_sql = f"""
        SELECT dm.modelo, dm.velocidade_cpu, dr.precisao
        FROM dados_ML dm
        JOIN dados_resultado dr ON dm.id_processamento = dr.id_processamento
        WHERE dm.id_processamento = {latest_proc_id};
        """
        data_row = fetchone(data_sql)

        fotos_dia_sql = "SELECT COUNT(id) AS fotos_dia FROM banco_imagens WHERE DATE(data_captura) = (SELECT DATE(MAX(data_captura)) FROM banco_imagens);"
        fotos_dia_row = fetchone(fotos_dia_sql)

        if not data_row: return {"modelo": "N/A", "fotos_dia": 0, "precisao_media_latest": "N/A", "velocidade_cpu_latest": "N/A"}

        precisao_formatted = f"{round(float(data_row['precisao']), 2)}%" if data_row['precisao'] is not None else "N/A"
        velocidade_formatted = f"{round(float(data_row['velocidade_cpu']), 1)} ms" if data_row['velocidade_cpu'] is not None else "N/A"

        return {
            "modelo": data_row['modelo'] if data_row['modelo'] else "Desconhecido",
            "fotos_dia": int(fotos_dia_row['fotos_dia']) if fotos_dia_row and fotos_dia_row['fotos_dia'] else 0,
            "precisao_media_latest": precisao_formatted,
            "velocidade_cpu_latest": velocidade_formatted,
        }
    except Exception as e:
        print(f"Erro em get_performance_data_latest: {e}")
        traceback.print_exc()
        return {"modelo": "ERRO", "fotos_dia": 0, "precisao_media_latest": "ERRO", "velocidade_cpu_latest": "ERRO"}

# Busca os dados de processamento ML (dados_ML e dados_resultado) mais recentes.
def get_recent_ml_processing(limit: int = 100000) -> List[Dict[str, Any]]:
    try:
        sql = """
        SELECT dm.id_processamento, dm.id_imagem, dm.data_processamento, dm.modelo, dm.velocidade_cpu, dr.precisao
        FROM dados_ML dm
        LEFT JOIN dados_resultado dr ON dm.id_processamento = dr.id_processamento
        ORDER BY dm.data_processamento DESC LIMIT %s;
        """
        rows = fetchall(sql, [limit])
        return [
            {
                "id_processamento": int(row['id_processamento']),
                "id_imagem": int(row['id_imagem']),
                "data_processamento": row['data_processamento'].strftime('%Y-%m-%d %H:%M:%S') if row['data_processamento'] else "N/A",
                "modelo": row['modelo'] if row['modelo'] else "N/A",
                "velocidade_cpu": f"{round(float(row['velocidade_cpu']), 1)} ms" if row['velocidade_cpu'] is not None else "N/A",
                "precisao": f"{round(float(row['precisao']) * 100, 2)}%" if row['precisao'] is not None else "N/A",
            }
            for row in rows
        ]
    except Exception as e:
        print(f"Erro em get_recent_ml_processing: {e}")
        traceback.print_exc()
        return []


# --- AGREGADORES ---

# Busca dados para página de Análises (M9 - M12).
def get_analises_data(time_filter: str) -> Dict[str, Any]:
    try:
        print(f"Buscando dados de Análise de Desempenho (M9 - M12) para: {time_filter}")
        m11_data = get_m11_precisao_diaria_chart(time_filter)
        dados = {
            "m12_taxa_captura": get_m12_taxa_captura_analise(time_filter),
            "m11_precisao_media": m11_data,
            "m9_velocidade_cpu": get_m9_velocidade_cpu(time_filter),
            "m10_quantidade_fotos_db": get_m10_quantidade_fotos_db("365 days"),
        }
        return dados
    except Exception as e:
        print(f"ERRO em get_analises_data: {e}")
        traceback.print_exc()
        return {}


# Busca todos os dados para o dashboard (M1 - M8 e M13).
def get_all_dashboard_data(time_filter: str) -> Dict[str, Any]:
    try:
        print(f"Buscando todos os dados do dashboard (M1 - M8 e M13) para: {time_filter}")
        dados = {
            "m1_quantidade_adultos_total": get_m1_quantidade_adultos_total(time_filter),
            "m2_distribuicao_ciclo_vida": get_m2_distribuicao_ciclo_vida(),
            "m3_taxa_mortalidade_diaria": get_m3_taxa_mortalidade_diaria(time_filter),
            "m4_necessidade_intervencao_area": get_m4_necessidade_intervencao_area(time_filter),
            "m5_taxa_captura_imagens_diaria": get_m5_taxa_captura_imagens_diaria(time_filter),
            "m6_quantidade_ovos_diario": get_m6_quantidade_ovos_diario(time_filter),
            "m7_taxa_ovop_por_adulto": get_m7_taxa_ovop_por_adulto(time_filter),
            "m8_taxa_crescimento": get_m8_taxa_crescimento_diaria(time_filter),
            "m13_reinocular_ovos": get_m13_reinocular_ovos(time_filter),
            "temp_media": {"valor": 26, "unidade": "°C"},
            "umidade_media": {"valor": 70, "unidade": "%"}
        }
        return dados
    except Exception as e:
        print(f"ERRO em get_all_dashboard_data: {e}")
        traceback.print_exc()
        return {}