"use client";

import type { TaskPlan } from "@/types/agent";
import { CheckCircle2, Circle, Loader2, XCircle } from "lucide-react";

function StatusIcon({ status }: { status: TaskPlan["status"] }) {
  switch (status) {
    case "done": return <CheckCircle2 size={16} className="text-green-500" />;
    case "running": return <Loader2 size={16} className="text-blue-500 animate-spin" />;
    case "failed": return <XCircle size={16} className="text-red-500" />;
    default: return <Circle size={16} className="text-gray-300" />;
  }
}

export function WorkflowTimeline({ plan }: { plan: TaskPlan[] }) {
  if (!plan.length) return null;

  return (
    <div className="bg-white rounded-xl border border-gray-100 p-6">
      <h3 className="text-sm font-semibold text-gray-900 mb-4">工作流</h3>
      <div className="flex items-center gap-2 flex-wrap">
        {plan.map((task, i) => (
          <div key={task.id} className="flex items-center gap-2">
            <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium ${
              task.status === "done" ? "bg-green-50 text-green-700" :
              task.status === "running" ? "bg-blue-50 text-blue-700" :
              task.status === "failed" ? "bg-red-50 text-red-700" :
              "bg-gray-50 text-gray-400"
            }`}>
              <StatusIcon status={task.status} />
              {task.name}
            </div>
            {i < plan.length - 1 && (
              <span className="text-gray-300 text-xs">→</span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
