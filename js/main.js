document.addEventListener('DOMContentLoaded', () => {
  // 
  //   dados ate então simulados.
  // 
  const realTimeElement = document.getElementById('realtimeInsetos');
  if (realTimeElement) {
    let currentInsetos = 3357;
    setInterval(() => {
      const change = Math.floor(Math.random() * 20) - 10; // +10 ou -10
      currentInsetos += change;
      realTimeElement.textContent = currentInsetos.toLocaleString('pt-BR');
    }, 3000); 
  }

  //   Gráfico simulado até escolhermos um framework e passar os dados corretos.

  // Dados de ex (Simulando formato JSON)
  const larvasData = {
    labels: [
      'Jan',
      'Fev',
      'Mar',
      'Abr',
      'Mai',
      'Jun',
      'Jul',
      'Ago',
      'Set',
      'Out',
    ],
    datasets: [
      {
        label: 'Real',
        data: [750, 820, 150, 300, 450, 380, 250, 780, 400, 600],
        backgroundColor: '#08654F',
        borderRadius: 5,
        barPercentage: 0.6,
      },
      {
        label: 'Ideal',
        data: [600, 700, 100, 450, 400, 500, 300, 700, 500, 750],
        backgroundColor: '#0AA146',
        borderRadius: 5,
        barPercentage: 0.6,
      },
    ],
  };

  const cicloVidaData = {
    labels: ['Ovo', 'Larva', 'Pupa', 'Adulta'],
    datasets: [
      {
        data: [1232, 810, 890, 425],
        backgroundColor: ['#08654F', '#0c8a3e', '#0AA146', '#3fba7a'],
        borderColor: 'rgba(0,0,0,0)',
        cutout: '70%',
      },
    ],
  };

  const metricaDesempenhoData1 = {
    labels: [0, 2, 4, 6, 8, 10, 12, 14, 16, 18],
    datasets: [
      {
        label: 'YOLOv8m',
        data: [38.5, 42, 48, 51.5, 52.5, 53, 53.2, 53.3, 53.3, 53.3],
        borderColor: '#08654F',
        backgroundColor: '#08654F',
        tension: 0.4,
        fill: false,
      },
      {
        label: 'YOLOv8s',
        data: [37, 40, 45, 48, 49, 49.5, 50, 50.1, 50.1, 50.1],
        borderColor: '#0AA146',
        backgroundColor: '#0AA146',
        tension: 0.4,
        fill: false,
      },
      {
        label: 'YOLOv5',
        data: [35, 38, 42, 45, 46, 46.5, 46.8, 47, 47, 47],
        borderColor: '#7B7B7B',
        backgroundColor: '#7B7B7B',
        tension: 0.4,
        fill: false,
      },
    ],
  };

  const metricaDesempenhoData2 = {
    labels: [0, 2, 4, 6, 8, 10, 12, 14, 16, 18],
    datasets: [
      {
        label: 'YOLOv8m',
        data: [50.1, 51.2, 52.3, 53.0, 53.5, 53.8, 54.0, 54.1, 54.1, 54.1],
        borderColor: '#08654F',
        backgroundColor: '#08654F',
        tension: 0.4,
        fill: false,
      },
      {
        label: 'YOLOv8s',
        data: [49, 50, 51, 51.5, 52, 52.2, 52.3, 52.4, 52.4, 52.4],
        borderColor: '#0AA146',
        backgroundColor: '#0AA146',
        tension: 0.4,
        fill: false,
      },
      {
        label: 'YOLOv5',
        data: [48, 48.5, 49, 49.5, 50, 50.2, 50.3, 50.4, 50.4, 50.4],
        borderColor: '#7B7B7B',
        backgroundColor: '#7B7B7B',
        tension: 0.4,
        fill: false,
      },
    ],
  };

 // Gráficos
  let larvasChartInstance,
    cicloVidaChartInstance,
    metrica1Instance,
    metrica2Instance;

  function initDashboardCharts() {
    const larvasCtx = document.getElementById('larvasChart');
    if (larvasCtx) {
      if (larvasChartInstance) larvasChartInstance.destroy();

      larvasChartInstance = new Chart(larvasCtx.getContext('2d'), {
        type: 'bar',
        data: larvasData,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            y: { beginAtZero: true, grid: { drawBorder: false } },
            x: { grid: { display: false } },
          },
        },
      });
    }

    const cicloVidaCtx = document.getElementById('cicloVidaChart');
    if (cicloVidaCtx) {
      if (cicloVidaChartInstance) cicloVidaChartInstance.destroy();
      cicloVidaChartInstance = new Chart(cicloVidaCtx.getContext('2d'), {
        type: 'doughnut',
        data: cicloVidaData,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
        },
      });
    }
  }

  function initAnalisesCharts() {
    const options = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          labels: { usePointStyle: true, boxWidth: 10 },
        },
      },
      scales: {
        y: { title: { display: true, text: 'Coco mAP (val)' } },
        x: {
          title: {
            display: true,
            text: 'Latency T4 TensorRT(8 FP16) (ms/img)',
          },
        },
      },
    };

    const metricaCtx1 = document.getElementById('metricaDesempenhoChart1');
    if (metricaCtx1) {
      if (metrica1Instance) metrica1Instance.destroy();
      metrica1Instance = new Chart(metricaCtx1.getContext('2d'), {
        type: 'line',
        data: metricaDesempenhoData1,
        options: options,
      });
    }

    const metricaCtx2 = document.getElementById('metricaDesempenhoChart2');
    if (metricaCtx2) {
      if (metrica2Instance) metrica2Instance.destroy();
      metrica2Instance = new Chart(metricaCtx2.getContext('2d'), {
        type: 'line',
        data: metricaDesempenhoData2,
        options: options,
      });
    }
  }


  if (document.getElementById('dashboardPage')) {
    initDashboardCharts();
  }

  if (document.getElementById('analisesPage')) {
    initAnalisesCharts();
  }
});
