import { STATUS_COLORS } from './config.js';

export function aplicarEfeitoAtualizacao(element) {
    if (element) {
        element.classList.add('updated');
        setTimeout(() => {
            element.classList.remove('updated');
        }, 500);
    }
}

export function applyStatus(element, status, isFooter = false) {
    if (!element) return;

    element.classList.remove(STATUS_COLORS.RED, STATUS_COLORS.ORANGE, STATUS_COLORS.YELLOW, STATUS_COLORS.GREEN, STATUS_COLORS.FOOTER_CRITICAL);

    if (isFooter) {
        if (status === 'PERIGO' || status === 'INCOMUM') {
            element.classList.add(STATUS_COLORS.FOOTER_CRITICAL);
        }
    } else {
        if (status === 'PERIGO') element.classList.add(STATUS_COLORS.RED);
        else if (status === 'INCOMUM') element.classList.add(STATUS_COLORS.ORANGE);
        else element.classList.add(STATUS_COLORS.GREEN);
    }
}

export function getKpiStatus(kpiId, value) {
    let status = 'NORMAL';
    let message = '';

    switch (kpiId) {
        case 'M1': 
            if (value < 100) {
                status = 'PERIGO';
                message = 'População de Adultos muito baixa.';
            } else if (value < 500) {
                status = 'INCOMUM';
                message = 'População requer atenção e reforço.';
            } else {
                status = 'NORMAL';
                message = 'População de Adultos está adequada.';
            }
            break;
        case 'M3':
            if (value > 35.0) {
                status = 'PERIGO';
                message = `Mortalidade em Perigo (${value.toFixed(2)}%).`;
            } else if (value >= 15.0) {
                status = 'INCOMUM';
                message = `Mortalidade Incomum (${value.toFixed(2)}%).`;
            } else {
                status = 'NORMAL';
                message = `Mortalidade Normal (${value.toFixed(2)}%).`;
            }
            break;
        case 'M6':
            if (value < 300) {
                status = 'PERIGO';
                message = 'Produção de Ovos muito baixa.';
            } else if (value < 1000) {
                status = 'INCOMUM';
                message = 'Produção de Ovos abaixo da meta.';
            } else {
                status = 'NORMAL';
                message = 'Produção de Ovos está ótima.';
            }
            break;
    }
    return { status, message };
}

export function updateDateFilterDisplay(filterValue) {
    const displayElement = document.querySelector('.date-picker span');
    if (!displayElement) return;

    const today = new Date();
    const startDate = new Date();
    const todayFormatted = today.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });

    let label = '';
    if (filterValue === '1 day') {
        label = `Últimas 24h (Até ${todayFormatted})`;
    } else {
        let days = parseInt(filterValue.split(' ')[0], 10);
        startDate.setDate(today.getDate() - days);
        const startFormatted = startDate.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });
        label = `De ${startFormatted} a ${todayFormatted}`;
    }

    displayElement.textContent = label;
}