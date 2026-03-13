document.addEventListener('DOMContentLoaded', function() {
    // Registrar o plugin de labels para todos os gráficos
    Chart.register(ChartDataLabels);

    const labelsAnimais = JSON.parse(document.getElementById('data-labels-animais').textContent);
    const valoresAnimais = JSON.parse(document.getElementById('data-valores-animais').textContent);
    const labelsVol = JSON.parse(document.getElementById('data-labels-voluntarios').textContent);
    const valoresVol = JSON.parse(document.getElementById('data-valores-voluntarios').textContent);

    // Gráfico de Animais (Pizza/Doughnut)
    new Chart(document.getElementById('chartAnimais'), {
        type: 'doughnut',
        data: {
            labels: labelsAnimais,
            datasets: [{
                data: valoresAnimais,
                backgroundColor: ['#5bc0de', '#3c763d', '#f0ad4e'],
                borderColor: '#f8f9fa',
                borderWidth: 3,
                hoverOffset: 25,
                hoverBackgroundColor: ['#8edff0', '#6aaf6c', '#f7cb82']
            }]
        },
        options: {
            maintainAspectRatio: false,
            cutout: '48%',
            layout: {
                padding: 10
            },
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        padding: 20,
                        boxWidth: 18,
                        boxHeight: 18,
                        font: {
                            size: 14
                        },
                        generateLabels: function(chart) {
                            const data = chart.data;
                            const dataset = data.datasets[0];
                            //  const total = dataset.data.reduce((a, b) => a + b, 0);

                            return data.labels.map((label, i) => {
                                const value = dataset.data[i];
                                //  const percentage = total ? Math.round((value / total) * 100) : 0;

                                return {
                                    text: `${label}: ${value}`, //(${percentage}%)
                                    fillStyle: dataset.backgroundColor[i],
                                    strokeStyle: dataset.backgroundColor[i],
                                    lineWidth: 1,
                                    hidden: !chart.getDataVisibility(i),
                                    index: i
                                };
                            });
                        }
                    }
                },
                tooltip: {
                    enabled: false
                },
                datalabels: {
                    color: '#fff',
                    anchor: 'center',
                    align: 'center',
                    offset: 0,
                    clamp: true,
                    clip: false,
                    textAlign: 'center',
                    font: {
                        weight: 'bold',
                        size: 12
                    },
                    formatter: (value, ctx) => {
                        const data = ctx.dataset.data;
                        const total = data.reduce((a, b) => a + b, 0);
                        const percentage = total ? Math.round((value / total) * 100) : 0;

                        return value > 0 ? `${percentage}%` : '';
                    }
                }
            }
        },
        plugins: [ChartDataLabels]
    });

    // Gráfico de Voluntários (Barras)
    new Chart(document.getElementById('chartVoluntarios'), {
        type: 'bar',
        data: {
            labels: labelsVol,
            datasets: [{
                data: valoresVol,
                backgroundColor: '#fd7e14',
                hoverBackgroundColor: '#ffb067'
            }]
        },
        options: {
            maintainAspectRatio: false,
            layout: { padding: { top: 30 } }, // Espaço para o número não cortar
            scales: {
                y: { beginAtZero: true, display: false }, // Esconde o eixo Y para limpar
                x: { grid: { display: false } }
            },
            plugins: {
                legend: { display: false },
                datalabels: {
                    anchor: 'end',
                    align: 'top',
                    color: '#444',
                    font: { weight: 'bold' },
                    formatter: Math.round
                },
                tooltip: {
                    enabled: false
                },
            }
        }
    });
});