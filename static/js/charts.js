// Custom Admin Analytics Charts (Chart.js implementation)

document.addEventListener('DOMContentLoaded', function() {
    // 1. Revenue Chart
    const revenueCtx = document.getElementById('revenueChart');
    if (revenueCtx) {
        // Read data attributes injected by Django views
        const months = JSON.parse(revenueCtx.dataset.months || '[]');
        const amounts = JSON.parse(revenueCtx.dataset.amounts || '[]');

        new Chart(revenueCtx, {
            type: 'line',
            data: {
                labels: months,
                datasets: [{
                    label: 'Monthly Revenue ($)',
                    data: amounts,
                    borderColor: '#c5a059',
                    backgroundColor: 'rgba(197, 160, 89, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)'
                        },
                        ticks: {
                            color: '#a0aec0'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#a0aec0'
                        }
                    }
                }
            }
        });
    }

    // 2. Booking Status Distribution Chart
    const statusCtx = document.getElementById('bookingStatusChart');
    if (statusCtx) {
        const statuses = JSON.parse(statusCtx.dataset.statuses || '[]');
        const counts = JSON.parse(statusCtx.dataset.counts || '[]');

        new Chart(statusCtx, {
            type: 'doughnut',
            data: {
                labels: statuses,
                datasets: [{
                    data: counts,
                    backgroundColor: [
                        '#ffd700', // Pending - Goldish
                        '#2ecc71', // Confirmed - Green
                        '#3498db', // Completed - Blue
                        '#e74c3c'  // Cancelled - Red
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#a0aec0',
                            padding: 15
                        }
                    }
                },
                cutout: '70%'
            }
        });
    }
});
