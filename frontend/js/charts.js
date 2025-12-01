import { CHART_COLORS, BASE_TOOLTIP_OPTS } from './config.js';

// Instâncias locais dos gráficos
let instances = {
    larvas: null,
    cicloVida: null,
    mortalidade: null,
    ovoposition: null,
    growthRate: null,
    precisaoMedia: null,
    ovosDiario: null
};

export function atualizarGraficoPrecisaoMedia(labels, data) {
    const ctx = document.getElementById("precisaoMediaChart");
    if (!ctx) return;

    if (instances.precisaoMedia) instances.precisaoMedia.destroy();

    instances.precisaoMedia = new Chart(ctx.getContext('2d'), {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Precisão Média (%)",
                data: data,
                borderColor: CHART_COLORS[5],
                backgroundColor: CHART_COLORS[5] + '33',
                fill: true,
                tension: 0.4,
                borderWidth: 3,
                pointRadius: 4,
                pointBackgroundColor: CHART_COLORS[5],
                pointHoverRadius: 6,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    ...BASE_TOOLTIP_OPTS,
                    callbacks: { label: (context) => ` Precisão: ${context.parsed.y.toFixed(2)}%` }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: { display: true, text: 'Precisão (%)', font: { family: 'Outfit', size: 14, weight: '500' } },
                    grid: { color: CHART_COLORS[6] + '1A', borderDash: [5, 5], drawBorder: false },
                    ticks: { callback: (value) => `${value}%`, font: { family: 'Outfit', size: 12 } }
                },
                x: {
                    grid: { display: false },
                    ticks: { font: { family: 'Outfit', size: 12 } }
                }
            }
        }
    });
}

export function atualizarGraficoLarvas(labels, necessaria, referencia) {
    const ctx = document.getElementById("larvasChart");
    if (!ctx) return;

    if (instances.larvas) instances.larvas.destroy();

    instances.larvas = new Chart(ctx.getContext('2d'), {
        type: "bar",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Área Necessária (m²)",
                    data: necessaria,
                    backgroundColor: CHART_COLORS[1],
                    borderRadius: 5,
                    barPercentage: 0.7,
                    categoryPercentage: 0.8,
                    yAxisID: 'y'
                },
                {
                    label: "Área Total (m²)",
                    data: referencia,
                    type: 'line',
                    borderColor: CHART_COLORS[6],
                    borderWidth: 2,
                    pointRadius: 0,
                    fill: false,
                    tension: 0.3,
                    yAxisID: 'y_ref'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: true, position: 'top' },
                tooltip: { ...BASE_TOOLTIP_OPTS }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: CHART_COLORS[6] + '1A', drawBorder: false },
                    title: { display: true, text: 'Área (m²)' },
                    ticks: { font: { family: 'Outfit', size: 12 } }
                },
                y_ref: { display: false },
                x: { grid: { display: false } }
            }
        }
    });
}

export function atualizarGraficoCicloVida(labels, data) {
    const ctx = document.getElementById("cicloVidaChart");
    if (!ctx) return;

    if (instances.cicloVida) instances.cicloVida.destroy();

    const customColors = [CHART_COLORS[0], CHART_COLORS[1], CHART_COLORS[0]];

    instances.cicloVida = new Chart(ctx.getContext('2d'), {
        type: "doughnut",
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: customColors,
                borderColor: 'rgba(0,0,0,0)',
                borderWidth: 0,
                cutout: "70%",
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            layout: { padding: 0 },
            plugins: {
                legend: { display: false },
                tooltip: {
                    ...BASE_TOOLTIP_OPTS,
                    callbacks: {
                        label: (context) => {
                            const value = context.parsed;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percent = total > 0 ? (value / total * 100).toFixed(1) : 0;
                            return ` ${context.label}: ${value.toLocaleString()} (${percent}%)`;
                        }
                    }
                }
            }
        }
    });

    // Atualiza legenda HTML se existir
    const legendContainer = document.getElementById('cicloVidaLegend');
    if (legendContainer) {
        const legendItems = legendContainer.querySelectorAll('.legend-item');
        if (legendItems.length >= 3) {
            legendItems[0].querySelector('.legend-color').style.backgroundColor = customColors[0];
            legendItems[1].querySelector('.legend-color').style.backgroundColor = customColors[1];
            legendItems[2].querySelector('.legend-color').style.backgroundColor = customColors[2];
        }
    }
}

export function atualizarGraficoMortalidade(labels, data) {
    const ctx = document.getElementById("mortalidadeChart");
    if (!ctx) return;

    if (instances.mortalidade) instances.mortalidade.destroy();

    instances.mortalidade = new Chart(ctx.getContext('2d'), {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Taxa de Mortalidade Média (%)",
                data: data,
                borderColor: CHART_COLORS[1],
                backgroundColor: CHART_COLORS[1] + '33',
                fill: 'origin',
                tension: 0.4,
                borderWidth: 3,
                pointRadius: 4,
                pointBackgroundColor: CHART_COLORS[1],
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: { ...BASE_TOOLTIP_OPTS, callbacks: { label: (c) => ` Taxa: ${c.parsed.y.toFixed(2)}%` } }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: { display: true, text: 'Mortalidade (%)' },
                    grid: { color: CHART_COLORS[6] + '1A', borderDash: [5, 5], drawBorder: false }
                },
                x: { grid: { display: false } }
            }
        }
    });
}

export function atualizarGraficoOvoposition(labels, data) {
    const ctx = document.getElementById("ovopositionChart");
    if (!ctx) return;
    if (instances.ovoposition) instances.ovoposition.destroy();

    instances.ovoposition = new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Ovos por Adulto',
                data: data,
                backgroundColor: CHART_COLORS[0],
                borderRadius: 5,
                barThickness: 15,
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: { ...BASE_TOOLTIP_OPTS, callbacks: { label: (c) => ` Taxa: ${c.parsed.x.toFixed(2)}` } }
            },
            scales: {
                x: { beginAtZero: true, title: { display: true, text: 'Ovos/Adulto' }, grid: { color: CHART_COLORS[6] + '1A', drawBorder: false } },
                y: { grid: { display: false } }
            }
        }
    });
}

export function atualizarGraficoOvosDiario(labels, data) {
    const ctx = document.getElementById("ovosDiarioChart");
    if (!ctx) return;

    if (instances.ovosDiario) instances.ovosDiario.destroy();
    
    const average = data.length > 0 ? data.reduce((a, b) => a + b) / data.length : 0;
    
    instances.ovosDiario = new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Média Diária de Ovos",
                    data: data,
                    borderColor: CHART_COLORS[1], 
                    backgroundColor: CHART_COLORS[1] + '33',
                    fill: 'origin',
                    tension: 0.3,
                    borderWidth: 3,
                    pointRadius: 4,
                    pointBackgroundColor: CHART_COLORS[1],
                    yAxisID: 'y'
                },
                {
                    label: "Média do Período",
                    data: labels.map(() => average),
                    borderColor: CHART_COLORS[7],
                    borderWidth: 1,
                    borderDash: [5, 5],
                    pointRadius: 0,
                    fill: false,
                    tension: 0,
                    yAxisID: 'y'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: true, position: 'top' },
                tooltip: { ...BASE_TOOLTIP_OPTS }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: { display: true, text: 'Contagem de Ovos' },
                    grid: { color: CHART_COLORS[6] + '1A', borderDash: [5, 5], drawBorder: false }
                },
                x: { grid: { display: false } }
            }
        }
    });
}

export function renderizarM8Chart(labels, rateData, adultCountData) {
    const ctx = document.getElementById("growthRateChart");
    if (!ctx) return;

    if (instances.growthRate) instances.growthRate.destroy();

    instances.growthRate = new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: `Taxa de Crescimento (%)`,
                    data: rateData,
                    borderColor: CHART_COLORS[1],
                    backgroundColor: CHART_COLORS[1] + '33',
                    yAxisID: 'y',
                    fill: false,
                    tension: 0.4,
                    borderWidth: 3,
                    pointRadius: 4,
                    pointBackgroundColor: CHART_COLORS[1]
                },
                {
                    label: `População de Adultos`,
                    data: adultCountData,
                    borderColor: CHART_COLORS[0],
                    backgroundColor: CHART_COLORS[0] + '33',
                    yAxisID: 'y1',
                    fill: false,
                    tension: 0.4,
                    borderWidth: 3,
                    pointRadius: 4,
                    pointBackgroundColor: CHART_COLORS[0]
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: true, position: 'top' },
                tooltip: { 
                    ...BASE_TOOLTIP_OPTS,
                    callbacks: {
                        label: (context) => {
                            if (context.datasetIndex === 0) return ` Crescimento: ${context.parsed.y.toFixed(2)}%`;
                            return ` População: ${context.parsed.y.toLocaleString("pt-BR")}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    position: 'left',
                    title: { display: true, text: 'Taxa de Crescimento (%)' },
                    grid: { color: CHART_COLORS[6] + '1A', borderDash: [5, 5], drawBorder: false },
                    ticks: { callback: (v) => `${v}%` }
                },
                y1: {
                    position: 'right',
                    beginAtZero: true,
                    title: { display: true, text: 'População de Adultos' },
                    grid: { drawOnChartArea: false }
                }
            }
        }
    });
}