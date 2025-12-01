import { getBaseUrl } from './config.js';
import { updateDateFilterDisplay } from './utils.js';
import { processarDadosDashboard } from './dashboard.js';
import { processarDadosAnalises, loadRecentImagesData, loadRecentMlData, loadLatestPerformanceData } from './analises.js';

let socket = null;
let isConnecting = false;

window.dashboardSocket = null;

export async function checkBackendHealth() {
    try {
        const response = await fetch(`${getBaseUrl()}/health`);
        return response.ok;
    } catch { return false; }
}

export async function connectWebSocket() {
    const WS_URL = window.WS_URL_GLOBAL; 
    let initialFilter = '7 days';

    if (!WS_URL) {
        console.error("WS_URL_GLOBAL não definido.");
        return;
    }

    if (window.dashboardSocket && window.dashboardSocket.readyState === WebSocket.OPEN) {
        socket = window.dashboardSocket;
        sendFilterUpdate(initialFilter);
        return;
    }

    if (isConnecting) return;
    isConnecting = true;

    socket = new WebSocket(WS_URL);
    window.dashboardSocket = socket;

    socket.onopen = () => {
        isConnecting = false;
        console.log("WebSocket conectado.");
        sendFilterUpdate(initialFilter);
        
        if (document.getElementById("analisesPage")) {
            loadLatestPerformanceData();
            loadRecentImagesData();
            loadRecentMlData();
        }
    };

    socket.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        
        if (msg.evento === "dashboard_full_update") {
            updateDateFilterDisplay(msg.filter || initialFilter);
            if (msg.dashboard) processarDadosDashboard(msg.dashboard);
            if (msg.analises) processarDadosAnalises(msg.analises);
        } else if (msg.evento === "nova_imagem_processada") {
            console.log(`Nova imagem processada: Gaiola ${msg.gaiola}`);
            if (document.getElementById("analisesPage")) {
                 loadRecentImagesData(); 
                 loadRecentMlData(); 
            }
        }
    };

    socket.onerror = (err) => {
        isConnecting = false;
        console.error("ERRO WebSocket", err);
    };

    socket.onclose = (event) => {
        isConnecting = false;
        window.dashboardSocket = null;
        if (event.code !== 1000) setTimeout(connectWebSocket, 3000);
    };
}

export function sendFilterUpdate(filterValue) {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ evento: "request_update", filter: filterValue }));
    }
}