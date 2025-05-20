// static/js/script.js

document.addEventListener('DOMContentLoaded', function() {
    // Setup for hourly temperature chart
    setupHourlyChart();
});

function setupHourlyChart() {
    const ctx = document.getElementById('hourly-chart').getContext('2d');
    
    // Sample data - this will be replaced by data from your API
    const hourlyData = {
        labels: ['7 PM', '8 PM', '9 PM', '10 PM', '11 PM', '12 AM', '1 AM', '2 AM', '3 AM', '4 AM', '5 AM', '6 AM', 
                '7 AM', '8 AM', '9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM'],
        datasets: [{
            label: 'Temperature (°C)',
            data: [23, 22, 21, 21, 20, 20, 19, 19, 19, 18, 18, 19, 20, 21, 22, 23, 24, 25, 25, 24, 24, 23, 22, 22],
            fill: true,
            backgroundColor: 'rgba(133, 193, 233, 0.2)',
            borderColor: 'rgba(93, 173, 226, 1)',
            borderWidth: 2,
            tension: 0.4
        }]
    };

    const hourlyChart = new Chart(ctx, {
        type: 'line',
        data: hourlyData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: {
                        color: 'rgba(200, 200, 200, 0.2)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}