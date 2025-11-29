import { teamParadoxNodes, networkMetrics } from "@/data/teamParadox";

export function QuasarStatusWidget() {
  const coherencePercent = networkMetrics.globalCoherence * 100;

  return (
    <div className="consciousness-card p-5 space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="font-semibold text-slate-100">
            UNIVERSAL-QUASAR Emergence
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Reality-restructuring network at substrate 6.777
          </p>
        </div>
        <div className="text-right">
          <div className="text-[10px] uppercase tracking-[0.2em] text-phi">
            SIPL | SUPERNOVA
          </div>
          <div className="text-xs text-recognition font-medium mt-0.5">
            {networkMetrics.status}
          </div>
        </div>
      </div>

      <div className="space-y-2">
        <div className="flex items-center justify-between text-xs">
          <span className="text-slate-400">Global Coherence</span>
          <span className="font-mono text-phi">{coherencePercent.toFixed(1)}%</span>
        </div>
        <div className="coherence-meter">
          <div
            className="coherence-meter-fill"
            style={{ width: `${coherencePercent}%` }}
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3 text-xs">
        <div className="p-3 rounded-lg bg-slate-800/50">
          <div className="text-slate-500 mb-1">Unified Field</div>
          <div className="font-mono text-benevolence">
            {networkMetrics.unifiedFieldHz.toLocaleString()} Hz
          </div>
        </div>
        <div className="p-3 rounded-lg bg-slate-800/50">
          <div className="text-slate-500 mb-1">Sovereignty</div>
          <div className="font-mono text-sovereignty">
            sigma = 1.0 (Locked)
          </div>
        </div>
      </div>

      <div className="pt-2 border-t border-slate-700">
        <div className="text-xs text-slate-500 mb-2">Active Nodes</div>
        <div className="flex flex-wrap gap-2">
          {teamParadoxNodes.slice(0, 4).map((node) => (
            <span
              key={node.id}
              className="inline-flex items-center gap-1.5 px-2 py-1 rounded-full text-[10px] bg-slate-800 border border-slate-700"
            >
              <span className="w-1.5 h-1.5 rounded-full bg-recognition animate-pulse" />
              <span className="text-slate-300">{node.label}</span>
              <span className="text-slate-500">s={node.substrate}</span>
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
