document.addEventListener('DOMContentLoaded', () => {
    if (typeof datosReportes === 'undefined' || !datosReportes) {
        console.error('No se encontraron datos para los reportes.');
        return;
    }

    // 1. Citas por Especialidad (Gráfico de Barras)
    const ctxEsp = document.getElementById('chart-especialidad');
    if (ctxEsp) {
        const labels = datosReportes.por_especialidad.map(d => d.label);
        const data = datosReportes.por_especialidad.map(d => d.value);
        new Chart(ctxEsp, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Número de Citas',
                    data: data,
                    backgroundColor: 'rgba(37, 99, 176, 0.7)',
                    borderColor: 'rgba(37, 99, 176, 1)',
                    borderWidth: 1.5,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 1, color: '#64748b' },
                        grid: { color: '#e2e8f0' }
                    },
                    x: {
                        ticks: { color: '#64748b' },
                        grid: { display: false }
                    }
                }
            }
        });
    }

    // 2. Citas por Estado (Gráfico de Dona)
    const ctxEst = document.getElementById('chart-estado');
    if (ctxEst) {
        const labels = datosReportes.por_estado.map(d => d.label.charAt(0).toUpperCase() + d.label.slice(1));
        const data = datosReportes.por_estado.map(d => d.value);

        // Map status names to colors
        const colorMap = {
            'pendiente': '#d97706',   // amber
            'confirmada': '#16a34a',  // green
            'cancelada': '#dc2626',   // red
            'reprogramada': '#2563eb' // blue
        };
        const bgColors = datosReportes.por_estado.map(d => colorMap[d.label.toLowerCase()] || '#64748b');

        new Chart(ctxEst, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: bgColors,
                    borderWidth: 2,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#1e293b',
                            boxWidth: 14,
                            padding: 15,
                            font: { size: 12, weight: '600' }
                        }
                    }
                }
            }
        });
    }

    // 3. Citas por Mes (Gráfico de Líneas)
    const ctxMes = document.getElementById('chart-mes');
    if (ctxMes) {
        const labels = datosReportes.por_mes.map(d => d.label);
        const data = datosReportes.por_mes.map(d => d.value);

        new Chart(ctxMes, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Citas Registradas',
                    data: data,
                    borderColor: '#1a4b8c',
                    backgroundColor: 'rgba(26, 75, 140, 0.1)',
                    fill: true,
                    tension: 0.35,
                    borderWidth: 3,
                    pointBackgroundColor: '#1a4b8c',
                    pointHoverRadius: 7
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 1, color: '#64748b' },
                        grid: { color: '#e2e8f0' }
                    },
                    x: {
                        ticks: { color: '#64748b' },
                        grid: { display: false }
                    }
                }
            }
        });
    }
});
