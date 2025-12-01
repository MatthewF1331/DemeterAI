import json
import traceback
from typing import List
from fastapi import WebSocket, WebSocketDisconnect
from services_metrics import get_all_dashboard_data, get_analises_data

# Gerencia conexões WebSocket ativas e permite broadcast
class ConnectionManager:
    def __init__(self):
        self.active: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active.append(websocket)
        print(f"WS conectado. Total: {len(self.active)}")

        default_filter = "7 days"
        dashboard_data = get_all_dashboard_data(default_filter)
        analises_data = get_analises_data(default_filter)

        await websocket.send_json({
            "evento": "dashboard_full_update",
            "filter": default_filter,
            "dashboard": dashboard_data,
            "analises": analises_data
        })

    def disconnect(self, websocket: WebSocket):
        try:
            self.active.remove(websocket)
        except ValueError:
            pass
        print(f"WS desconectado. Total: {len(self.active)}")

    # Envia um JSON para todos os clients conectados
    async def broadcast_json(self, message: dict):
        living = []
        for ws in list(self.active):
            try:
                await ws.send_json(message)
                living.append(ws)
            except Exception as e:
                pass
        self.active = living

# Comunicação Websocket
async def handle_websocket(websocket: WebSocket, manager: ConnectionManager):
    await manager.connect(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            try:
                msg = json.loads(message)
                if msg.get("evento") == "request_update" and "filter" in msg:
                    time_filter = msg["filter"]
                    print(f"WS: Recebido pedido de atualização com filtro: {time_filter}")
                    dashboard_data = get_all_dashboard_data(time_filter)
                    analises_data = get_analises_data(time_filter)

                    response_payload = {
                        "evento": "dashboard_full_update",
                        "filter": time_filter,
                        "dashboard": dashboard_data,
                        "analises": analises_data
                    }
                    await manager.broadcast_json(response_payload)
                else:
                    print("WS: Mensagem recebida sem evento ou filtro esperado.")
            except json.JSONDecodeError:
                print(f"WS: Mensagem recebida não é JSON: {message}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)