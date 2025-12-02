import time
from ultralytics import YOLO
import cv2
import os
import json
import psycopg2
import requests
from psycopg2.extras import RealDictCursor 

# CONFIGURAÇÕES DE DIRETÓRIOS

input_dir = "../dataset/iot/input"
processed_dir = "../dataset/iot/processed"
error_dir = "../dataset/iot/error"

os.makedirs(input_dir, exist_ok=True)
os.makedirs(processed_dir, exist_ok=True)
os.makedirs(error_dir, exist_ok=True)

# ----- CONFIGURAÇÃO DO BANCO & BACKEND --------

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "port": os.getenv("DB_PORT", "5432"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASS", "postgres"),
    "dbname": os.getenv("DB_NAME", "demeter"),
}

# URL para notificar o backend via HTTP POST
BACKEND_NOTIFY_URL = os.getenv("BACKEND_NOTIFY_URL", "http://backend:8000/notify")

# ---------- FUNÇÕES DO BANCO -----------

# Retorna uma nova conexão ativa com o PostgreSQL
def get_conn():
    return psycopg2.connect(**DB_CONFIG)


# Retorna a próxima imagem a ser processada após last_id
def get_next_image(last_id):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, caminho_arquivo
            FROM banco_imagens
            WHERE id > %s
            ORDER BY id ASC
            LIMIT 1
        """, (last_id,))
        row = cur.fetchone()
        return row if row else (None, None)
    finally:
        cur.close()
        conn.close()


# Retorna o último id_imagem já processado pelo ML
def get_last_processed_image():
    conn = get_conn()
    cur = conn.cursor()
    try:
        # Usa COALESCE para garantir que retorna 0 se a tabela estiver vazia
        cur.execute("SELECT COALESCE(MAX(id_imagem), 0) FROM dados_ML")
        row = cur.fetchone()
        return row[0]
    finally:
        cur.close()
        conn.close()


def insert_ml_result(id_imagem, origem, previsao, velocidade_cpu, versao, parametros):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO dados_ML (id_imagem, modelo, previsao_media, velocidade_cpu, versao_modelo, parametros)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_processamento
        """, (id_imagem, origem, previsao, velocidade_cpu, versao, json.dumps(parametros))) # Garante que 'parametros' é JSON
        new_id = cur.fetchone()[0]
        conn.commit()
        return new_id
    finally:
        cur.close()
        conn.close()


def insert_processed_result(id_processamento, sexo, quantidade, etapa, precisao):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO dados_resultado (id_processamento, sexo, quantidade_insetos, etapa_ciclo, precisao)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_processamento, sexo, quantidade, etapa, precisao))
        conn.commit()
    finally:
        cur.close()
        conn.close()

try:
    # Usando a Versão 4 (train4)
    model = YOLO("../runs/detect/train4/weights/best.pt")
    MODEL_NAME = os.path.basename(model.predictor.model.pt) if model.predictor and model.predictor.model else "YOLOv8-Custom"
except Exception as e:
    print(f"ERRO ao carregar modelo YOLO. Verifique o caminho e permissões: {e}")
    MODEL_NAME = "YOLOv8-DUMMY"
    class DummyModel:
        def __call__(self, *args, **kwargs):
            class DummyBoxes:
                cls = []
                conf = []
                def __len__(self): return 0
            
            class DummyResult:
                boxes = DummyBoxes()
                speed = {'inference': 150.0, 'preprocess': 10.0, 'postprocess': 5.0} 
                def plot(self): return cv2.imread(caminho_arquivo)
            
            return [DummyResult()]
        names = {"0": "BL_adulto", "1": "BL_ovo"} 
    model = DummyModel()

# LOOP WHILE TRUE --------------------------------------------------
ultimo_id_processado = get_last_processed_image()
print(f"Último ID processado encontrado no banco: {ultimo_id_processado}")

while True:
    # --- Ponto de busca do próximo item ---
    result_fetch = get_next_image(ultimo_id_processado)
    id_imagem, nome_arquivo = result_fetch if result_fetch else (None, None)

    if not id_imagem:
        novo_ultimo_id = get_last_processed_image()
        if novo_ultimo_id > ultimo_id_processado:
            ultimo_id_processado = novo_ultimo_id
            print(f"Ponteiro de busca atualizado para ID: {ultimo_id_processado}")
        
        time.sleep(1)
        continue

    caminho_arquivo = os.path.join(input_dir, nome_arquivo)

    if not os.path.exists(caminho_arquivo):
        print(f"Arquivo {caminho_arquivo} NÃO EXISTE. Avançando ponteiro para {id_imagem}.")
        # Se o arquivo não existe no disco, o ponteiro avança para evitar loop
        ultimo_id_processado = id_imagem 
        continue

    print(f"\n----------------------------------------------------------------------------")
    print(f"INICIANDO PROCESSAMENTO: ID: {id_imagem}, Arquivo: {nome_arquivo}")
    print(f"----------------------------------------------------------------------------")

    try:
        # ---- PROCESSAR YOLO ----
        results = model(caminho_arquivo, verbose=False) 
        
        result = results[0]

        velocidade_cpu_ms = result.speed.get('inference', 0.0) 
        
        annotated_img = result.plot()
        boxes = result.boxes

        detected = boxes is not None and len(boxes) > 0

        # Contagem de classes
        adults = sum(1 for c in boxes.cls if model.names.get(int(c)) == "BL_adulto") if detected else 0
        eggs = sum(1 for c in boxes.cls if model.names.get(int(c)) == "BL_ovo") if detected else 0
        
        total_detections = adults + eggs

        # ---- PRECISÃO  ----
        precisao = 0.0
        if detected and len(boxes.conf) > 0:
            sum_conf = sum(conf.item() for conf in boxes.conf)
            precisao = round(sum_conf / len(boxes.conf), 4)
        else:
            precisao = 0.98
            
        # ---- NOMES DOS ARQUIVOS -----
        prefixo = "P" if detected else "E"
        destino_dir = processed_dir if detected else error_dir
        # Troca o prefixo I por P ou E
        novo_nome = prefixo + nome_arquivo[1:]
        destino_path = os.path.join(destino_dir, novo_nome)
        
        cv2.imwrite(destino_path, annotated_img)

        # ---- DADOS PARA DADOS_ML ----
        versao_modelo = "0.1" 
        
        parametros_json = {
            "raw_boxes": len(boxes) if detected else 0,
            "tempos_inferencia": result.speed,
            "modelo_base_nome": MODEL_NAME
        }

        id_processamento = insert_ml_result(
            id_imagem,
            MODEL_NAME,
            round(float(total_detections), 2), 
            round(velocidade_cpu_ms, 3),
            versao_modelo,
            parametros_json
        )

        # ---- DADOS PARA DADOS_RESULTADO ----
        etapa = (
            "Adulto" if adults > eggs and adults > 0 else 
            "Ovo" if eggs > adults and eggs > 0 else 
            "Múltiplo" if adults > 0 and eggs > 0 else 
            "Nenhum"
        )

        sexo = "N" 
        quantidade_insetos = total_detections
        
        insert_processed_result(
            id_processamento,
            sexo,
            quantidade_insetos,
            etapa,
            round(precisao, 2) 
        )

        print(f"   Model utilizado: {MODEL_NAME} (v{versao_modelo})")
        print(f"   Velocidade de inferência: {round(velocidade_cpu_ms, 3)} ms")
        print(f"   Detecções totais: {total_detections}")
        print(f"   - Adultos: {adults}")
        print(f"   - Ovos: {eggs}")
        print(f"   Fase Principal: {etapa}")
        print(f"   Precisão Média: {round(precisao, 2)}")
        print(f"   Status: {'Processado' if detected else 'Erro/Nenhum Inseto Detectado'}")
        print(f"   Processamento CONCLUÍDO - ID: {id_processamento}")


        # NOTIFICAR O BACKEND
        try:
            response = requests.post(
                BACKEND_NOTIFY_URL,
                json={
                    "id_imagem": id_imagem,
                    "id_processamento": id_processamento
                },
                timeout=2
            )
            response.raise_for_status() 
            print(f"Notificação enviada com sucesso ao backend (status={response.status_code})")

        except requests.exceptions.RequestException as notify_error:
            print(f"ERRO ao notificar backend. O backend está rodando? Erro: {notify_error}")

    except Exception as e:
        print(f"ERRO crítico ao processar {nome_arquivo}: {e}")
        # Move o arquivo para diretório de erro
        novo_nome = "E" + nome_arquivo[1:]
        dest_err = os.path.join(error_dir, novo_nome)
        if os.path.exists(caminho_arquivo):
            os.rename(caminho_arquivo, dest_err)
        print(f"Arquivo movido para erro: {dest_err}")
        print(f"--------------------------------------------------------------------\n")

    # Atualiza ponteiro para o próximo ciclo
    ultimo_id_processado = id_imagem