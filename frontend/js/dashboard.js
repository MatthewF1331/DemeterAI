import { CHART_COLORS, STATUS_COLORS, FILTER_MAP } from './config.js';
import { applyStatus, getKpiStatus, aplicarEfeitoAtualizacao, updateDateFilterDisplay } from './utils.js';
import * as Charts from './charts.js';
import { sendFilterUpdate } from './websocket.js';

let m8RawData = { cages: [], data_map: {} };
let currentM8CageId = null;

export function setupDateFilters() {
    const filterButtons = document.querySelectorAll(".date-filters .btn");
    filterButtons.forEach(btn => {
        const filterKey = btn.textContent.trim();
        const filterValue = FILTER_MAP[filterKey];
        if (filterValue) {
            btn.addEventListener("click", () => applyDateFilter(btn, filterValue));
        }
    });
    updateDateFilterDisplay('7 days');
}

function applyDateFilter(filterButton, filterValue) {
    const container = filterButton.closest('.date-filters');
    if (container) {
        container.querySelectorAll(".btn").forEach(b => b.classList.remove("active"));
        filterButton.classList.add("active");
    }
    sendFilterUpdate(filterValue);
}

export function processarDadosDashboard(dados) {
    if (!dados) return;

    const els = {
        m1Value: document.getElementById("m1-value"),
        m1Footer: document.getElementById("m1-footer"),
        m1Indicator: document.getElementById("m1-indicator"),
        m3Value: document.getElementById("m3-value"),
        m3Footer: document.getElementById("m3-footer"),
        m3Indicator: document.getElementById("m3-indicator"),
        m4Value: document.getElementById("m4-value"),
        m5Value: document.getElementById("m5-value"),
        m6Value: document.getElementById("m6-value"),
        m6Unit: document.getElementById("m6-unit"),
        m6Footer: document.getElementById("m6-footer"),
        m6Indicator: document.getElementById("m6-indicator"),
        m7ValueKpi: document.getElementById("m7-value-kpi"),
        m13Value: document.getElementById("m13-value"), 
        m13Footer: document.getElementById("m13-footer"), 
        doughnutTotal: document.getElementById("doughnut-total"),
        doughnutFooter: document.getElementById("doughnut-footer"),
        m8CageSelector: document.getElementById("m8-cage-selector")
    };

    // M1 ----------------
    const m1 = dados.m1_quantidade_adultos_total;
    if (els.m1Value) {
        const m1Status = getKpiStatus('M1', m1.valor);
        els.m1Value.textContent = m1.valor.toLocaleString("pt-BR");
        els.m1Footer.textContent = m1Status.message || (m1.gaiolas > 0 ? `Total em ${m1.gaiolas} gaiolas.` : `Sem dados.`);
        applyStatus(els.m1Indicator, m1Status.status);
        applyStatus(els.m1Footer, m1Status.status, true);
        aplicarEfeitoAtualizacao(els.m1Value);
    }

    // M2 ----------------
    const m2 = dados.m2_distribuicao_ciclo_vida;
    const labelsM2 = ["Ovo", "Larva", "Pupa", "Adulto"];
    const ovos = m2.data[labelsM2.indexOf("Ovo")] || 0;
    const adultos = m2.data[labelsM2.indexOf("Adulto")] || 0;
    const outros = (m2.data[labelsM2.indexOf("Larva")] || 0) + (m2.data[labelsM2.indexOf("Pupa")] || 0);
    
    Charts.atualizarGraficoCicloVida(["Ovo", "Adulto", "Outros"], [ovos, adultos, outros]);

    if (els.doughnutTotal) {
        const total = m2.data.reduce((a, b) => a + b, 0);
        els.doughnutTotal.innerHTML = `${total.toLocaleString("pt-BR")} <i class='bx bxs-bug-alt'></i>`;
    }

    // M3 ----------------
    const m3 = dados.m3_taxa_mortalidade_diaria;
    Charts.atualizarGraficoMortalidade(m3.labels, m3.data);
    if (els.m3Value) {
        const m3Status = getKpiStatus('M3', m3.kpi_valor);
        els.m3Value.textContent = `${m3.kpi_valor.toFixed(2)}%`;
        els.m3Footer.textContent = m3Status.message;
        applyStatus(els.m3Indicator, m3Status.status);
        applyStatus(els.m3Footer, m3Status.status, true);
        aplicarEfeitoAtualizacao(els.m3Value);
    }

    // M4 ----------------
    const m4 = dados.m4_necessidade_intervencao_area;
    Charts.atualizarGraficoLarvas(m4.labels, m4.area_necessaria, m4.area_referencia);
    if (els.m4Value) {
        els.m4Value.textContent = `${m4.kpi_valor.toFixed(1)}%`;
        aplicarEfeitoAtualizacao(els.m4Value);
    }

    // M5 ----------------
    if (els.m5Value) {
        els.m5Value.textContent = dados.m5_taxa_captura_imagens_diaria.kpi_valor.toLocaleString("pt-BR");
        aplicarEfeitoAtualizacao(els.m5Value);
    }

    // M6 -----------------
    const m6 = dados.m6_quantidade_ovos_diario;
    if (els.m6Value) {
        const m6Status = getKpiStatus('M6', m6.valor);
        els.m6Value.textContent = m6.valor.toLocaleString("pt-BR");
        els.m6Unit.textContent = m6.unidade;
        els.m6Footer.textContent = m6Status.message;
        applyStatus(els.m6Indicator, m6Status.status);
        applyStatus(els.m6Footer, m6Status.status, true);
        aplicarEfeitoAtualizacao(els.m6Value);
    }
    Charts.atualizarGraficoOvosDiario(m6.labels, m6.data);

    // M7 ----------------
    const m7 = dados.m7_taxa_ovop_por_adulto;
    Charts.atualizarGraficoOvoposition(m7.labels, m7.data);
    if (els.m7ValueKpi) {
        els.m7ValueKpi.textContent = m7.kpi_valor.toFixed(2);
        els.m7ValueKpi.style.color = CHART_COLORS[4];
    }

    // M8 ----------------
    m8RawData = dados.m8_taxa_crescimento;
    if (els.m8CageSelector) inicializarM8Seletor(els.m8CageSelector);

    // M13 ---------------
    const m13 = dados.m13_reinocular_ovos;
    if (els.m13Value) {
        let status = m13.status === "CRÍTICO" ? 'PERIGO' : m13.status === "ATENÇÃO" ? 'INCOMUM' : 'NORMAL';
        els.m13Value.style.color = status === 'PERIGO' ? STATUS_COLORS.RED : status === 'INCOMUM' ? STATUS_COLORS.ORANGE : STATUS_COLORS.GREEN;
        els.m13Value.textContent = `${m13.volume_estimado_ml.toFixed(2)} ${m13.unidade}`;
        els.m13Footer.textContent = `Meta: ${m13.volume_target_ml.toFixed(1)} ${m13.unidade}. Status: ${m13.status}.`;
        applyStatus(els.m13Footer, status, true);
        aplicarEfeitoAtualizacao(els.m13Value);
    }
}

function inicializarM8Seletor(selector) {
    if (!selector || m8RawData.cages.length === 0) {
        if (selector) selector.innerHTML = '<option value="">Sem Gaiolas Ativas</option>';
        return;
    }
    
    selector.innerHTML = '';
    m8RawData.cages.forEach(cageId => {
        const option = document.createElement('option');
        option.value = cageId;
        option.textContent = `Gaiola ${cageId}`;
        selector.appendChild(option);
    });

    if (!currentM8CageId) currentM8CageId = m8RawData.cages[0];
    selector.value = currentM8CageId;

    // Clonar para limpar listeners antigos
    const newSelector = selector.cloneNode(true);
    selector.parentNode.replaceChild(newSelector, selector);
    
    newSelector.addEventListener('change', (event) => {
        currentM8CageId = event.target.value;
        renderM8Chart(currentM8CageId);
    });

    renderM8Chart(currentM8CageId);
}

function renderM8Chart(cageId) {
    const dataForCage = m8RawData.data_map[cageId];
    if (!dataForCage) return;
    Charts.renderizarM8Chart(dataForCage.labels, dataForCage.data, dataForCage.adult_count);
}