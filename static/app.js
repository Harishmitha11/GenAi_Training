document.addEventListener('DOMContentLoaded', () => {
    const runBtn = document.getElementById('run-pipeline-btn');
    const loadingOverlay = document.getElementById('loading-overlay');
    const reportSection = document.getElementById('report-section');

    const steps = {
        extract: document.getElementById('step-extract'),
        pandas: document.getElementById('step-pandas'),
        langchain: document.getElementById('step-langchain'),
        load: document.getElementById('step-load')
    };

    runBtn.addEventListener('click', async () => {
        // Reset UI Context
        reportSection.classList.add('hidden');
        loadingOverlay.classList.remove('hidden');
        runBtn.disabled = true;
        runBtn.textContent = 'Processing...';

        Object.values(steps).forEach(s => {
            s.className = 'step';
        });

        // Start animating steps sequentially just for UI indication
        steps.extract.classList.add('active');

        try {
            // Fake animation progression while fetching
            setTimeout(() => { steps.extract.classList.replace('active', 'completed'); steps.pandas.classList.add('active'); }, 500);
            setTimeout(() => { steps.pandas.classList.replace('active', 'completed'); steps.langchain.classList.add('active'); }, 1500);

            // API Call
            const response = await fetch('/api/etl/run', {
                method: 'POST'
            });

            const data = await response.json();

            // Finish animations
            steps.langchain.classList.replace('active', 'completed');
            steps.load.classList.add('completed');

            if (response.ok) {
                renderReport(data.report, data.visualizations);
            } else {
                handleError(data.message || 'Pipeline failed', data.audit);
            }
        } catch (error) {
            handleError(error.message, []);
        } finally {
            loadingOverlay.classList.add('hidden');
            runBtn.disabled = false;
            runBtn.textContent = 'Run Default Dataset';
        }
    });

    let deptChartInstance = null;
    let ageChartInstance = null;

    function renderReport(report, visualizations) {
        document.getElementById('metric-duration').textContent = `${report.duration_seconds.toFixed(2)}s`;
        document.getElementById('metric-in').textContent = report.metrics.input_rows;
        document.getElementById('metric-out').textContent = report.metrics.output_rows;
        document.getElementById('metric-nulls').textContent = report.metrics.nulls_handled;

        const terminal = document.getElementById('audit-terminal');
        terminal.innerHTML = ''; // clear

        report.audit_trail.forEach(log => {
            const entry = document.createElement('div');
            entry.className = 'log-entry';

            const time = new Date(log.timestamp).toLocaleTimeString();
            let detailsStr = JSON.stringify(log.details, null, 2).replace(/\\n/g, '<br>');

            entry.innerHTML = `
                <span class="log-time">[${time}]</span>
                <span class="log-step">${log.step}</span>
                <span class="log-status status-${log.status}">[${log.status}]</span>
                <span class="log-details">${detailsStr}</span>
            `;
            terminal.appendChild(entry);
        });

        if (visualizations) {
            renderCharts(visualizations);
        }

        reportSection.classList.remove('hidden');
        // Scroll to report
        setTimeout(() => {
            reportSection.scrollIntoView({ behavior: 'smooth' });
        }, 100);
    }

    function renderCharts(viz) {
        if (deptChartInstance) deptChartInstance.destroy();
        if (ageChartInstance) ageChartInstance.destroy();

        const deptCtx = document.getElementById('deptChart').getContext('2d');
        deptChartInstance = new Chart(deptCtx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(viz.departments),
                datasets: [{
                    data: Object.values(viz.departments),
                    backgroundColor: ['#FF6B6B', '#4facfe', '#43e97b', '#fa709a', '#f59e0b', '#8b5cf6'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8' } } }
            }
        });

        const ageCtx = document.getElementById('ageChart').getContext('2d');
        ageChartInstance = new Chart(ageCtx, {
            type: 'bar',
            data: {
                labels: Object.keys(viz.ages),
                datasets: [{
                    label: 'Users',
                    data: Object.values(viz.ages),
                    backgroundColor: '#6366f1',
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                    x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                }
            }
        });
    }

    function handleError(msg, auditLogs) {
        alert("Error executing pipeline: " + msg);
        Object.values(steps).forEach(s => {
            if (s.classList.contains('active')) {
                s.classList.replace('active', 'error');
            }
        });
        if (auditLogs && auditLogs.length > 0) {
            renderReport({
                duration_seconds: 0,
                metrics: { input_rows: '?', output_rows: '?', nulls_handled: '?' },
                audit_trail: auditLogs
            });
        }
    }
});
