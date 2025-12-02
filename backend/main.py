import os
import traceback
from typing import Optional

from fastapi import FastAPI, WebSocket, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from config import IMAGE_ROOT_PATH, CORS_ORIGINS
from database import get_conn  # Só pra Health Check
from services_metrics import (
    get_all_dashboard_data, 
    get_analises_data, 
    get_performance_data_latest, 
    get_recent_ml_processing
)
from services_images import (
    get_all_images_summary, 
    get_image_details, 
    get_recent_images_data
)
from websocket_manager import ConnectionManager, handle_websocket


# -------- CONFIGURAÇÃO E INICIALIZAÇÃO -----------

app = FastAPI(title="DemeterAI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = ConnectionManager()


# -------- MODELS E BACKGROUND TASKS -----------

#Esquema de dados para o endpoint /notify (recebido do ML)
class NotifyRequest(BaseModel):
    id_imagem: int
    id_processamento: int

#Função de background que busca dados de processamento e faz broadcast
async def process_and_broadcast(id_processamento: int, manager: ConnectionManager, time_filter: str = "7 days"):
    try:
        dashboard_update = {
            "evento": "dashboard_full_update",
            "filter": time_filter,
            "dashboard": get_all_dashboard_data(time_filter),
            "analises": get_analises_data(time_filter)
        }
        await manager.broadcast_json(dashboard_update)
    except Exception as e:
        print(f"Erro em _process_and_broadcast: {e}")
        traceback.print_exc()


# -------- ROTAS HTTP ----------

# ENDPOINT HTTP chamado pelo ML para notificar um novo resultado
@app.post("/notify")
async def notify_new_result(payload: NotifyRequest, background_tasks: BackgroundTasks):
    try:
        if not payload.id_processamento or payload.id_processamento <= 0:
            raise HTTPException(status_code=400, detail="id_processamento inválido")

        background_tasks.add_task(process_and_broadcast, payload.id_processamento, manager)
        return {"status": "ok", "message": "Notificação recebida e processamento em background iniciado."}
    except Exception as e:
        print(f"Erro no endpoint notify: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

#ENDPOINT HTTP para listar as imagens com resumo de processamento com filtro de pesquisa
@app.get("/database/images")
async def get_database_images(search_query: Optional[str] = Query(None)):
    try:
        images_summary = get_all_images_summary(search_query=search_query)
        return images_summary
    except Exception as e:
        print(f"Erro no endpoint /database/images: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar lista de imagens.")

#ENDPOINT HTTP para buscar os detalhes de uma imagem específica
@app.get("/database/image/{image_id}")
async def get_database_image_details(image_id: int):
    try:
        details = get_image_details(image_id)
        if not details:
            raise HTTPException(status_code=404, detail="Imagem não encontrada.")
        return details
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Erro no endpoint /database/image/{image_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar detalhes da imagem.")

# ENDPOINT HTTP para servir arquivos de imagem estaticamente
@app.get("/images/{file_name}")
async def serve_image(file_name: str):
    if ".." in file_name or "/" in file_name or "\\" in file_name:
        raise HTTPException(status_code=400, detail="Nome de arquivo inválido.")

    file_prefix = file_name[0].upper()
    if file_prefix == 'I':
        sub_folder = 'input'
    elif file_prefix == 'P':
        sub_folder = 'processed'
    else:
        sub_folder = 'input' 

    full_sub_path = os.path.join(IMAGE_ROOT_PATH, sub_folder)
    file_path = os.path.join(full_sub_path, file_name)
    
    print(f"DEBUG: Tentando servir imagem '{file_name}'. Base Path: {IMAGE_ROOT_PATH}. Path primário: {file_path}")

    fallback_path = None
    if not os.path.exists(file_path):
        print(f"AVISO: Arquivo não encontrado no caminho primário: {file_path}")
        opposite_sub_folder = 'input' if sub_folder == 'processed' else 'processed'
        fallback_path = os.path.join(IMAGE_ROOT_PATH, opposite_sub_folder, file_name)
        print(f"DEBUG: Tentando fallback no caminho: {fallback_path}")

        if os.path.exists(fallback_path):
            file_path = fallback_path
            print(f"SUCESSO: Usando caminho de fallback: {file_path}")
        else:
            final_error_message = f"Arquivo '{file_name}' não encontrado no servidor."
            print(f"ERRO 404: {final_error_message}")
            raise HTTPException(status_code=404, detail=final_error_message)

    return FileResponse(file_path)

@app.get("/analises/performance/latest")
async def get_analises_performance_latest_route():
    try:
        return get_performance_data_latest()
    except Exception as e:
        print(f"Erro no endpoint /analises/performance/latest: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar dados de desempenho fixos.")

@app.get("/analises/recent-images")
async def get_analises_recent_images_route():
    try:
        return get_recent_images_data() 
    except Exception as e:
        print(f"Erro no endpoint /analises/recent-images: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar dados de imagens recentes.")

@app.get("/analises/all-ml-processing")
async def get_analises_all_ml_processing_route():
    try:
        return get_recent_ml_processing() 
    except Exception as e:
        print(f"Erro no endpoint /analises/all-ml-processing: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar dados de processamento ML.")

# ENDPOINT para verificar saúde da aplicação e conexão com BD
@app.get("/")
@app.get("/health")
async def health_check():
    conn = None
    try:
        conn = get_conn()
        return {"status": "healthy", "database": "connected", "app": "DemeterAI Backend"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": f"Erro de conexão com DB: {str(e)}"}
    finally:
        if conn:
            conn.close()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await handle_websocket(websocket, manager)