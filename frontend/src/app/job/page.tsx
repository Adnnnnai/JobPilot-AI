"use client";

import { useState } from "react";
import { useAgent } from "@/hooks/useAgent";
import { WorkflowTimeline } from "@/components/WorkflowTimeline";
import { Briefcase, Search, Loader2, CheckCircle2, AlertCircle } from "lucide-react";

export default function JobPage() {
  const { loading, plan, invoke } = useAgent();
  const [keyword, setKeyword] = useState("AI Agent开发工程师");
  const [result, setResult] = useState<Record<string, unknown> | null>(null);

  const handleSearch = async () => {
    setResult(null);
    const res = await invoke({
      message: `帮我搜索${keyword}岗位并匹配`,
      resume_path: "D:/project/JobPilot-AI/uploads/zhangsan.docx",
      jd: keyword,
      thread_id: "job_" + Date.now(),
      resume_id: 8,
      approved: false,
    });
    if (res) {
      // Parse match_result from response
      let match = {};
      if (res.match_result) {
        try { match = typeof res.match_result === "string" ? JSON.parse(res.match_result) : res.match_result; } catch {}
      }
      setResult({ ...res, match });
    }
  };

  return (
    <div className="space-y-6 max-w-5xl">
      <h1 className="text-2xl font-bold text-gray-900">岗位匹配</h1>
      <div className="bg-white rounded-xl border border-gray-100 p-4 flex gap-3">
        <div className="flex-1 flex items-center gap-2 px-3 py-2 bg-gray-50 rounded-lg">
          <Search size={16} className="text-gray-400" />
          <input value={keyword} onChange={e => setKeyword(e.target.value)}
            className="bg-transparent text-sm outline-none w-full" placeholder="搜索岗位关键词..." />
        </div>
        <button onClick={handleSearch} disabled={loading}
          className="px-4 py-2 bg-gray-900 text-white rounded-lg text-sm font-medium disabled:opacity-50 flex items-center gap-2">
          {loading && <Loader2 size={16} className="animate-spin" />}
          搜索并匹配
        </button>
      </div>
      <WorkflowTimeline plan={plan} />
      {result && (
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-white rounded-xl border border-gray-100 p-5">
            <h3 className="text-sm font-semibold text-gray-900 mb-3 flex items-center gap-2"><Briefcase size={16} /> 返回结果</h3>
            <pre className="text-xs text-gray-600 whitespace-pre-wrap max-h-96 overflow-auto">{JSON.stringify(result, null, 2).slice(0, 2000)}</pre>
          </div>
          <div className="space-y-4">
            <div className="bg-white rounded-xl border border-gray-100 p-5 text-center">
              <div className="text-5xl font-bold text-gray-900">{
                (result as Record<string,unknown>).match?.score ?? (result as Record<string,unknown>).match?.match_score ?? "?"
              }%</div>
              <div className="text-sm text-gray-500 mt-1">匹配度</div>
            </div>
            {(result as Record<string,unknown>).match?.matched_skills && (
              <div className="bg-white rounded-xl border border-gray-100 p-4">
                <h4 className="text-xs font-semibold text-green-600 mb-2 flex items-center gap-1"><CheckCircle2 size={14} /> 已匹配技能</h4>
                <div className="flex flex-wrap gap-1.5">{((result as Record<string,unknown>).match?.matched_skills as string[])?.map((s: string) => <span key={s} className="px-2 py-0.5 bg-green-50 text-green-700 rounded text-xs">{s}</span>)}</div>
              </div>
            )}
            {(result as Record<string,unknown>).match?.missing_skills && (
              <div className="bg-white rounded-xl border border-gray-100 p-4">
                <h4 className="text-xs font-semibold text-red-600 mb-2 flex items-center gap-1"><AlertCircle size={14} /> 缺失技能</h4>
                <div className="flex flex-wrap gap-1.5">{((result as Record<string,unknown>).match?.missing_skills as string[])?.map((s: string) => <span key={s} className="px-2 py-0.5 bg-red-50 text-red-700 rounded text-xs">{s}</span>)}</div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
