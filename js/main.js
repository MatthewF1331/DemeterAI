document.addEventListener('DOMContentLoaded', () => {

    const mockData = {
        larvas: {
            labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out'],
            ideal: [740, 80, 450, 370, 500, 800, 420, 520, 800, 800],
            real: [850, 290, 510, 250, 220, 650, 390, 610, 280, 520]
        },
        cicloVida: {
            labels: ['Ovo', 'Larva', 'Pupa', 'Adulta'],
            data: [1232, 890, 425, 810] // Ordem: Ovo, Larva, Pupa, Adulta
        },
        analises: {
            yolo11: [{x: 1.5, y: 39.5}, {x: 2.3, y: 47}, {x: 5.8, y: 53.3}, {x: 11.2, y: 54.8}],
            yolo10: [{x: 1.5, y: 37.5}, {x: 2.5, y: 45}, {x: 6.5, y: 50.2}, {x: 9.5, y: 53}, {x: 14.5, y: 54}]
        }
    };

    // --- PREPARAÇÃO PARA API DO MATEUS ---
    /*
    
    const socket = new WebSocket('wss://api.demeter.com/stream');

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        
        // atualiza o contador
        if (data.tipo === 'insetos_vivos') {
            atualizarContador(data.valor);
        }

        // atualiza graficos
        if (data.tipo === 'novo_ciclo') {
            atualizarGraficoRosca(data.ciclo);
        }
    };

    // func pra buscar os dados na api(REST API)
    async function fetchDashboardData() {
        try {
            const response = await fetch('https://api.demeter.com/dashboard');
            const data = await response.json();
            return data; // Retorna dados reais
        } catch (error) {
            console.error("Erro ao buscar dados:", error);
            return mockData; // Usa dados falsos se a API falhar
        }
    }
    */

    const realTimeElement = document.getElementById('realtimeInsetos');
    
    
    function atualizarContador(novoValor) {
        if (realTimeElement) {
            realTimeElement.textContent = novoValor.toLocaleString('pt-BR');
        }
    }

    if(realTimeElement) {
        let currentInsetos = 3357;
        setInterval(() => {
            const change = Math.floor(Math.random() * 20) - 10; 
            currentInsetos += change;
            atualizarContador(currentInsetos);
        }, 3000);
    }


    const larvasData = {
        labels: mockData.larvas.labels,
        datasets: [
            { 
                label: 'Ideal', 
                data: mockData.larvas.ideal, 
                backgroundColor: '#08654F', 
                borderRadius: 4,
                barPercentage: 0.6,
                categoryPercentage: 0.8
            },
            { 
                label: 'Real', 
                data: mockData.larvas.real, 
                backgroundColor: '#0AA146', 
                borderRadius: 4,
                barPercentage: 0.6,
                categoryPercentage: 0.8
            }
        ]
    };
    
    const cicloVidaData = {
        labels: mockData.cicloVida.labels,
        datasets: [{
            data: mockData.cicloVida.data,
            backgroundColor: [
                '#0AA146', // Ovo
                '#044735', // Larva
                '#00E640', // Pupa
                '#5D8E82'  // Adulta
            ], 
            borderWidth: 0,
            cutout: '70%'
        }]
    };

    const metricaDesempenhoData1 = {
        datasets: [
            { 
                label: 'YOLO11', 
                data: mockData.analises.yolo11, 
                borderColor: '#1E3A8A', 
                backgroundColor: '#1E3A8A', 
                borderWidth: 2.5, 
                tension: 0.4, 
                pointRadius: 5, 
                showLine: true 
            },
            { 
                label: 'YOLOv10', 
                data: mockData.analises.yolo10, 
                borderColor: '#FCA5A5', 
                backgroundColor: '#FCA5A5', 
                borderWidth: 2.5, 
                tension: 0.4, 
                pointRadius: 5, 
                showLine: true 
            }
        ]
    };
    
    const metricaDesempenhoData2 = {
        labels: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 
        datasets: [
            { label: 'YOLOv8m', data: [50, 51, 52.5, 53, 53.5, 53.8, 54, 54.1, 54.1, 54.1], borderColor: '#065F46', backgroundColor: '#065F46', borderWidth: 2.5, tension: 0.4, pointRadius: 3, fill: false },
            { label: 'YOLOv8s', data: [49, 50, 51, 51.5, 52, 52.2, 52.3, 52.4, 52.4, 52.4], borderColor: '#10B981', backgroundColor: '#10B981', borderWidth: 2.5, tension: 0.4, pointRadius: 3, fill: false },
            { label: 'YOLOv5', data: [48, 48.5, 49, 49.5, 50, 50.2, 50.3, 50.4, 50.4, 50.4], borderColor: '#6B7280', backgroundColor: '#6B7280', borderWidth: 2.5, tension: 0.4, pointRadius: 3, fill: false }
        ]
    };


    function initDashboardCharts() {
        const larvasCtx = document.getElementById('larvasChart');
        if (larvasCtx) {
            // vc chama fetchDashboardData() antes de criar o gráfico
            new Chart(larvasCtx.getContext('2d'), {
                type: 'bar', 
                data: larvasData,
                options: { 
                    responsive: true, 
                    maintainAspectRatio: false, 
                    plugins: { legend: { display: false } }, 
                    scales: { 
                        y: { beginAtZero: true, grid: { color: '#f0f0f0' }, border: {display: false}, max: 1000 }, 
                        x: { grid: { display: false }, border: {display: false} } 
                    } 
                } 
            });
        }

        const cicloVidaCtx = document.getElementById('cicloVidaChart');
        if (cicloVidaCtx) {
            new Chart(cicloVidaCtx.getContext('2d'), {
                type: 'doughnut', 
                data: cicloVidaData,
                options: { 
                    responsive: true, 
                    maintainAspectRatio: false, 
                    plugins: { legend: { display: false } } 
                } 
            });
        }
    }
    
    function initAnalisesCharts() {
        const commonScales = {
            y: { title: { display: true, text: 'COCO mAP 50-95', color: '#9CA3AF', font: {size: 10} }, min: 36, max: 56, grid: { color: '#F3F4F6' }, ticks: { color: '#6B7280', stepSize: 2 } },
            x: { type: 'linear', title: { display: true, text: 'Latency T4 TensorRT10 FP16(ms/img)', color: '#9CA3AF', font: {size: 10} }, min: 0, max: 18, grid: { color: '#F3F4F6' }, ticks: { color: '#6B7280', stepSize: 2 } }
        };

        const metricaCtx1 = document.getElementById('metricaDesempenhoChart1');
        if (metricaCtx1) {
            new Chart(metricaCtx1.getContext('2d'), { type: 'scatter', data: metricaDesempenhoData1, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: commonScales } });
        }

        const metricaCtx2 = document.getElementById('metricaDesempenhoChart2');
        if (metricaCtx2) {
            new Chart(metricaCtx2.getContext('2d'), { type: 'line', data: metricaDesempenhoData2, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: true, position: 'bottom', align: 'end', labels: { boxWidth: 12, usePointStyle: true } } }, scales: { ...commonScales, x: { ...commonScales.x, type: 'category' } } } });
        }
    }

    if (document.getElementById('dashboardPage')) {
        initDashboardCharts();
    }
    if (document.getElementById('analisesPage')) {
        initAnalisesCharts();
    }
});