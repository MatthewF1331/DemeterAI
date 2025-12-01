export function getBaseUrl() {
    return "http://localhost:8000";
}

// Mapeamento dos botões para o valor de filtro de tempo
export const FILTER_MAP = {
    'Dia': '1 day',
    'Semana': '7 days',
    'Mês': '30 days'
};

export const CHART_COLORS = [
    '#0AA146',
    '#08654F',
    '#34D399',
    '#10B981',
    '#059669',
    '#6366F1',
    '#000000',
    '#7B7B7B',
];

// Classes de status para indicadores
export const STATUS_COLORS = {
    GREEN: 'status-green',
    YELLOW: 'status-yellow',
    ORANGE: 'status-orange',
    RED: 'status-red',
    FOOTER_CRITICAL: 'footer-critical'
};

// Configuração base de Tooltip do Chart.js
export const BASE_TOOLTIP_OPTS = {
    backgroundColor: CHART_COLORS[1],
    titleFont: { family: 'Outfit', size: 14, weight: '600' },
    bodyFont: { family: 'Outfit', size: 14, weight: '500' },
    borderColor: CHART_COLORS[0],
    borderWidth: 1,
    boxPadding: 4,
    cornerRadius: 6,
    padding: 10,
};