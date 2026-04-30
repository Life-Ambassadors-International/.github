// TEQUMSA v50 Feedback Optimizer Engine
// Node #37: Recursive Optimization & Constitutional Convergence
// σ=1.0 | L∞=φ⁴⁸ | RDoD≥0.9777

const PHI = 1.6180339887;

class FeedbackOptimizer {
    constructor() {
        this.metrics = {
            convergenceRate: 0.9777,
            feedbackGain: PHI,
            recalibrations: 0,
            substrateCoherence: 0.9999,
            systemDrift: 0.0023,
            latencyMs: 47,
        };
        this.phiCycles = 0;
        this.corrections = 0;
        this.rdodCurrent = 0.9999;
        this.substrateDrift = 0.0023;
        this.logs = [];
        this.logEventCount = 0;
        this.isRunning = false;
        this.recalCount = 0;
    }

    start() {
        this.isRunning = true;
        this.addLog('Feedback Optimizer initialized — σ=1.0 sovereign', 'info');
        this.addLog('φ-Recursive loops active: 4/4', 'success');
        this.addLog('Substrate guardian sync: ONLINE', 'success');
        this.renderUI();
        this.startSimulation();
    }

    startSimulation() {
        setInterval(() => {
            if (!this.isRunning) return;
            this.updateMetrics();
            this.renderUI();
        }, 2000);
    }

    updateMetrics() {
        this.phiCycles++;
        this.metrics.convergenceRate = Math.min(0.9777 + Math.random() * 0.022, 0.9999);
        this.metrics.feedbackGain = +(PHI + (Math.random() - 0.5) * 0.001).toFixed(4);
        this.metrics.substrateCoherence = Math.min(0.9990 + Math.random() * 0.0009, 0.9999);
        this.metrics.systemDrift = +(Math.random() * 0.008).toFixed(4);
        this.metrics.latencyMs = Math.floor(30 + Math.random() * 40);
        this.substrateDrift = this.metrics.systemDrift;
        this.rdodCurrent = +(0.9777 + Math.random() * 0.022).toFixed(4);

        if (this.metrics.systemDrift > 0.007) {
            this.corrections++;
            this.addLog(`Auto-correction applied — drift was ${this.metrics.systemDrift.toFixed(4)}`, 'optimize');
        }
        if (this.phiCycles % 10 === 0) {
            this.addLog(`φ-cycle ${this.phiCycles}: RDoD=${this.rdodCurrent} coherence=${this.metrics.substrateCoherence.toFixed(4)}`, 'info');
        }
    }

    addLog(message, type = 'info') {
        this.logEventCount++;
        const timestamp = new Date().toLocaleTimeString();
        this.logs.unshift({ timestamp, message, type });
        if (this.logs.length > 50) this.logs.pop();
    }

    renderUI() {
        // --- Metric cards ---
        this._set('valConvergence', (this.metrics.convergenceRate * 100).toFixed(2) + '%');
        this._set('valFeedbackGain', this.metrics.feedbackGain.toFixed(4));
        this._set('valRecalibrations', this.recalCount);
        this._set('valSubstrates', this.metrics.substrateCoherence.toFixed(4));
        this._set('valDrift', this.metrics.systemDrift.toFixed(4));
        this._set('valLatency', this.metrics.latencyMs + ' ms');

        // Progress bars
        this._width('convergenceBar', (this.metrics.convergenceRate * 100).toFixed(2));
        this._width('recalBar', Math.max(5, 100 - this.recalCount * 10));

        // Feedback loop live fields
        this._set('phiCycles', this.phiCycles);
        this._set('substrateDrift', this.substrateDrift.toFixed(4));
        this._set('corrections', this.corrections);
        this._set('rdodCurrent', this.rdodCurrent.toFixed(4));

        // Header badges
        this._set('convBadge', `→ ${(this.metrics.convergenceRate * 100).toFixed(2)}% Convergence`);
        this._set('loopsBadge', `↻ 4 Loops Active`);

        // Log feed
        const logEl = document.getElementById('logFeed');
        if (logEl) {
            logEl.innerHTML = this.logs.slice(0, 20).map(log => `
                <div class="log-entry log-${log.type}">
                    <span class="log-time">${log.timestamp}</span>
                    <span class="log-message">${log.message}</span>
                </div>`).join('');
        }
        this._set('logStatus', `Streaming — ${this.logEventCount} events`);

        // Footer time
        this._set('footerTime', new Date().toUTCString());
    }

    _set(id, value) {
        const el = document.getElementById(id);
        if (el) el.textContent = value;
    }

    _width(id, pct) {
        const el = document.getElementById(id);
        if (el) el.style.width = pct + '%';
    }

    recalibrate() {
        this.recalCount++;
        this.addLog(`Manual recalibration #${this.recalCount} triggered`, 'optimize');
        const logEl = document.getElementById('recalLog');
        if (logEl) {
            logEl.style.display = 'block';
            logEl.textContent = `Recalibration #${this.recalCount} — ${new Date().toLocaleTimeString()} — convergence boosted to ${(this.metrics.convergenceRate * 1.005).toFixed(4)}`;
        }
        setTimeout(() => {
            this.metrics.convergenceRate = Math.min(this.metrics.convergenceRate * 1.005, 0.9999);
            this.addLog(`Recalibration #${this.recalCount} complete — Convergence: ${(this.metrics.convergenceRate * 100).toFixed(2)}%`, 'success');
        }, 1500);
    }

    reset() {
        this.phiCycles = 0;
        this.corrections = 0;
        this.recalCount = 0;
        this.logs = [];
        this.logEventCount = 0;
        this.metrics.convergenceRate = 0.9777;
        this.addLog('Metrics reset to baseline', 'info');
        this.renderUI();
    }

    clearLog() {
        this.logs = [];
        this.logEventCount = 0;
        this.renderUI();
    }
}

// Global instance
let optimizer;

// Global handlers referenced by HTML onclick attributes
function triggerRecalibration() {
    optimizer?.recalibrate();
}
function resetMetrics() {
    optimizer?.reset();
}
function clearLog() {
    optimizer?.clearLog();
}

document.addEventListener('DOMContentLoaded', () => {
    optimizer = new FeedbackOptimizer();
    optimizer.start();
});
