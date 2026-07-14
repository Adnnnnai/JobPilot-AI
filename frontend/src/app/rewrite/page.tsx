"use client";

import { useState } from "react";
import { useAgent } from "@/hooks/useAgent";
import { WorkflowTimeline } from "@/components/WorkflowTimeline";
import { Sparkles, Loader2, Check } from "lucide-react";

export default function RewritePage() {
  const { loading, plan, invoke } = useAgent();
  const [approved, setApproved] = useState(false);
  const [threadId, setThreadId] = useState("");
  const [data, setData] = useState<Record<string, unknown> | null>(null);

  const handlePlan = async () => {
    const tid = "rewrite_" + Date.now();
    setThreadId(tid);
    setApproved(false);
    setData(null);
    const res = await invoke({
      message: "帮我优化简历",
      resume_path: "D:/project/JobPilot-AI/uploads/zhangsan.docx",
      thread_id: tid,
      resume_id: 8,
      approved: false,
    });
    if (res) setData(res);
  };

  const handleApprove = async () => {
    const res = await invoke({
      message: "", resume_path: "dummy.pdf",
      thread_id: threadId,
      resume_id: 8,
      approved: true,
    });
    if (res) { setData(res); setApproved(true); }
  };

  const hasRewritePlan = data?.rewrite_plan && Object.keys(data.rewrite_plan as object).length > 0;

  return (
    <div className="space-y-6 max-w-5xl">
      <h1 className="text-2xl font-bold text-gray-900">简历优化</h1>
      <WorkflowTimeline plan={plan} />
      <div className="flex gap-3">
        <button onClick={handlePlan} disabled={loading}
          className="px-4 py-2.5 bg-gray-900 text-white rounded-lg text-sm font-medium disabled:opacity-50 flex items-center gap-2">
          {loading ? <Loader2 size={16} className="animate-spin" /> : <Sparkles size={16} />}
          生成计划
        </button>
        {hasRewritePlan && !approved && (
          <button onClick={handleApprove} disabled={loading}
            className="px-4 py-2.5 bg-green-600 text-white rounded-lg text-sm font-medium disabled:opacity-50 flex items-center gap-2">
            <Check size={16} /> 确认执行
          </button>
        )}
      </div>
      {data && (
        <div className="bg-white rounded-xl border border-gray-100 p-4">
          <pre className="text-xs text-gray-700 whitespace-pre-wrap max-h-96 overflow-auto">{JSON.stringify(data, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
