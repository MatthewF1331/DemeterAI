import { getBaseUrl } from './config.js';
import { aplicarEfeitoAtualizacao } from './utils.js';
import { atualizarGraficoPrecisaoMedia } from './charts.js';

const els = {
    m12Value: document.getElementById("m12-value"),
    m9Value: document.getElementById("m9-value"),
    m10Value: document.getElementById("m10-value"),
    m11Value: document.getElementById("m11-value"),
    perfModelo: document.getElementById("perf-modelo"),
    perfFotosDia: document.getElementById("perf-fotos-dia"),
    perfPrecisaoMedia: document.getElementById("perf-precisao-media"),
    perfVelocidadeCpu: document.getElementById("perf-velocidade-cpu"),
    recentImagesTableBody: document.getElementById("recentImagesTableBody"), 
    totalImagesCount: document.getElementById("totalImagesCount"),
    recentMlTableBody: document.getElementById("recentMlTableBody"),
    totalMlCount: document.getElementById("totalMlCount"),
};

export function initAnalisesPage() {
    loadLatestPerformanceData();
    loadRecentImagesData(); 
    loadRecentMlData(); 
}

export function processarDadosAnalises(dados) {
    if (!dados) return;

    if (els.m12Value && dados.m12_taxa_captura) {
        els.m12Value.textContent = dados.m12_taxa_captura.valor.toLocaleString("pt-BR");
        aplicarEfeitoAtualizacao(els.m12Value);
    }
    if (els.m9Value && dados.m9_velocidade_cpu) {
        els.m9Value.textContent = dados.m9_velocidade_cpu.valor.toFixed(1);
        aplicarEfeitoAtualizacao(els.m9Value);
    }
    if (els.m10Value && dados.m10_quantidade_fotos_db) {
        els.m10Value.textContent = dados.m10_quantidade_fotos_db.valor.toLocaleString("pt-BR");
        aplicarEfeitoAtualizacao(els.m10Value);
        const header = document.getElementById("totalFotosHeader");
        if(header) header.textContent = dados.m10_quantidade_fotos_db.valor.toLocaleString("pt-BR");
    }

    // M11 - Precisão
    const m11 = dados.m11_precisao_media;
    if (m11) {
        const kpiValorCorrigido = m11.kpi_valor * 100;
        if (els.m11Value) {
            els.m11Value.textContent = kpiValorCorrigido.toFixed(2);
            aplicarEfeitoAtualizacao(els.m11Value);
        }
        if (m11.data) {
            const dataCorrigida = m11.data.map(val => val * 100);
            atualizarGraficoPrecisaoMedia(m11.labels, dataCorrigida);
        }
    }
}

export async function loadLatestPerformanceData() {
    try {
        const response = await fetch(`${getBaseUrl()}/analises/performance/latest`);
        if (!response.ok) throw new Error('Falha ao buscar performance.');
        const data = await response.json();

        if (els.perfModelo) els.perfModelo.textContent = data.modelo || 'N/A';
        if (els.perfFotosDia) els.perfFotosDia.textContent = data.fotos_dia.toLocaleString("pt-BR");
        if (els.perfPrecisaoMedia) els.perfPrecisaoMedia.textContent = data.precisao_media_latest;
        if (els.perfVelocidadeCpu) els.perfVelocidadeCpu.textContent = data.velocidade_cpu_latest;

    } catch (error) {
        console.error("Erro dados performance:", error);
    }
}

export async function loadRecentImagesData() {
    if (!els.recentImagesTableBody) return;
    els.recentImagesTableBody.innerHTML = `<tr><td colspan="6" class="text-center p-4"><i class='bx bx-loader bx-spin'></i> Carregando...</td></tr>`;

    try {
        const response = await fetch(`${getBaseUrl()}/analises/recent-images`);
        if (!response.ok) throw new Error('Erro ao buscar imagens.');
        const images = await response.json();

        if (images && images.length > 0) {
            let html = '';
            images.forEach(img => {
                const dateParts = img.data_captura ? img.data_captura.split(' ') : ['-','-'];
                const formattedDate = dateParts[0].split('-').reverse().join('/') + ' ' + dateParts[1];
                
                html += `
                    <tr>
                        <td><a href="database-detalhes.html?id=${img.id}" style="color: #3B82F6; text-decoration: underline;">${img.id}</a></td>
                        <td>${img.nome_arquivo || 'N/A'}</td>
                        <td>${formattedDate}</td>
                        <td class="font-bold">${img.gaiola}</td>
                        <td>${img.localizacao}</td>
                        <td>${img.tamanho}</td>
                    </tr>
                `;
            });
            els.recentImagesTableBody.innerHTML = html;
            if(els.totalImagesCount) els.totalImagesCount.textContent = `(${images.length} Total)`;
        } else {
            els.recentImagesTableBody.innerHTML = `<tr><td colspan="6" class="text-center p-4">Nenhuma imagem encontrada.</td></tr>`;
        }
    } catch (error) {
        els.recentImagesTableBody.innerHTML = `<tr><td colspan="6" class="text-center text-red-500 p-4">Erro: ${error.message}</td></tr>`;
    }
}

export async function loadRecentMlData() {
    if (!els.recentMlTableBody) return;
    els.recentMlTableBody.innerHTML = `<tr><td colspan="6" class="text-center p-4"><i class='bx bx-loader bx-spin'></i> Carregando...</td></tr>`;

    try {
        const response = await fetch(`${getBaseUrl()}/analises/all-ml-processing`);
        if (!response.ok) throw new Error('Erro ao buscar ML.');
        const mlData = await response.json();

        if (mlData && mlData.length > 0) {
            let html = '';
            mlData.forEach(proc => {
                const dateParts = proc.data_processamento ? proc.data_processamento.split(' ') : ['-','-'];
                const formattedDate = dateParts[0].split('-').reverse().join('/') + ' ' + dateParts[1];
                
                const val = parseFloat(proc.precisao.replace('%', ''));
                const color = val >= 90 ? '#10B981' : val >= 70 ? '#F59E0B' : '#EF4444';

                html += `
                    <tr>
                        <td>${proc.id_processamento}</td>
                        <td><a href="database-detalhes.html?id=${proc.id_imagem}" style="color: #3B82F6; text-decoration: underline;">${proc.id_imagem}</a></td>
                        <td>${formattedDate}</td>
                        <td>${proc.modelo}</td>
                        <td>${proc.velocidade_cpu}</td>
                        <td style="color: ${color}; font-weight: 600;">${proc.precisao}</td>
                    </tr>
                `;
            });
            els.recentMlTableBody.innerHTML = html;
            if(els.totalMlCount) els.totalMlCount.textContent = `(${mlData.length} Total)`;
        } else {
            els.recentMlTableBody.innerHTML = `<tr><td colspan="6" class="text-center p-4">Nenhum dado ML.</td></tr>`;
        }
    } catch (error) {
        els.recentMlTableBody.innerHTML = `<tr><td colspan="6" class="text-center text-red-500 p-4">Erro: ${error.message}</td></tr>`;
    }
}