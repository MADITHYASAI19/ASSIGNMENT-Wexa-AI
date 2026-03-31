/**
 * StockFlow Intelligence Matrix (Chart.js Integration with Real Data)
 */

// Chart data passed from backend
let chartData = window.chartData || {
    distribution: { labels: ['No Data'], data: [1] },
    trend: { labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], data: [0, 0, 0, 0, 0, 0] },
    performance: { labels: [], data: [] }
};

document.addEventListener('DOMContentLoaded', () => {
    initCharts();
});

function initCharts() {
    const isDark = !document.body.classList.contains('light-mode');
    const textColor = isDark ? '#94A3B8' : '#64748B';
    const gridColor = isDark ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.05)';

    // Generate colors based on data length
    const baseColors = ['#6366F1', '#A855F7', '#10B981', '#F59E0B', '#EF4444', '#3B82F6', '#EC4899', '#8B5CF6'];
    const chartColors = chartData.distribution.labels.map((_, i) => baseColors[i % baseColors.length]);

    // 1. Stock Distribution (Doughnut Chart)
    const ctxPie = document.getElementById('distribution-chart')?.getContext('2d');
    if (ctxPie) {
        new Chart(ctxPie, {
            type: 'doughnut',
            data: {
                labels: chartData.distribution.labels,
                datasets: [{
                    data: chartData.distribution.data,
                    backgroundColor: chartColors,
                    borderWidth: 0,
                    hoverOffset: 20
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { 
                        position: 'bottom', 
                        labels: { 
                            color: textColor, 
                            font: { family: 'Inter', size: 11 },
                            padding: 20,
                            usePointStyle: true
                        } 
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = total > 0 ? Math.round((value / total) * 100) : 0;
                                return `${label}: ${value} units (${percentage}%)`;
                            }
                        }
                    }
                },
                cutout: '65%'
            }
        });
    }

    // 2. Inventory Value Trend (Line Chart)
    const ctxLine = document.getElementById('value-trend-chart')?.getContext('2d');
    if (ctxLine) {
        new Chart(ctxLine, {
            type: 'line',
            data: {
                labels: chartData.trend.labels,
                datasets: [{
                    label: 'System Valuation ($)',
                    data: chartData.trend.data,
                    borderColor: '#6366F1',
                    backgroundColor: (context) => {
                        const ctx = context.chart.ctx;
                        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
                        gradient.addColorStop(0, 'rgba(99, 102, 241, 0.3)');
                        gradient.addColorStop(1, 'rgba(99, 102, 241, 0)');
                        return gradient;
                    },
                    fill: true,
                    tension: 0.4,
                    pointRadius: 6,
                    pointBackgroundColor: '#6366F1',
                    pointBorderColor: isDark ? '#0F172A' : '#FFFFFF',
                    pointBorderWidth: 2,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                scales: {
                    x: { 
                        grid: { display: false }, 
                        ticks: { color: textColor, font: { family: 'Inter' } } 
                    },
                    y: { 
                        grid: { color: gridColor }, 
                        ticks: { 
                            color: textColor,
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        } 
                    }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return 'Value: $' + context.parsed.y.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    }

    // 3. Product Performance (Bar Chart)
    const ctxBar = document.getElementById('performance-chart')?.getContext('2d');
    if (ctxBar && chartData.performance.labels.length > 0) {
        new Chart(ctxBar, {
            type: 'bar',
            data: {
                labels: chartData.performance.labels,
                datasets: [{
                    label: 'Turnover Rate',
                    data: chartData.performance.data,
                    backgroundColor: (context) => {
                        const value = context.raw;
                        if (value >= 80) return 'rgba(16, 185, 129, 0.8)';
                        if (value >= 50) return 'rgba(99, 102, 241, 0.8)';
                        return 'rgba(245, 158, 11, 0.8)';
                    },
                    borderRadius: 8,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { 
                        grid: { display: false }, 
                        ticks: { 
                            color: textColor,
                            font: { family: 'Inter', size: 10 },
                            maxRotation: 45
                        } 
                    },
                    y: { 
                        grid: { color: gridColor }, 
                        ticks: { color: textColor },
                        min: 0,
                        max: 100
                    }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return 'Efficiency: ' + context.parsed.y + '%';
                            }
                        }
                    }
                }
            }
        });
    } else if (ctxBar) {
        // Show empty state message
        ctxBar.canvas.parentElement.innerHTML = `
            <div class="flex flex-col items-center justify-center h-full text-center">
                <i data-lucide="bar-chart-2" class="w-12 h-12 text-text-muted mb-4"></i>
                <p class="text-sm text-text-secondary">No performance data available</p>
                <p class="text-xs text-text-muted mt-2">Add products to see turnover metrics</p>
            </div>
        `;
        lucide.createIcons();
    }
}
