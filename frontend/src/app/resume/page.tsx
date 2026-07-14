"use client";

import { useState } from "react";
import { useAgent } from "@/hooks/useAgent";
import { WorkflowTimeline } from "@/components/WorkflowTimeline";
import { Upload, FileText, Loader2 } from "lucide-react";
import { resumeApi } from "@/services/api";

export default function ResumePage() {
  const { loading, plan, invoke } = useAgent();
  const [uploading, setUploading] = useState(false);
  const [resumeId, setResumeId] = useState(8);
  const [parsed, setParsed] = useState<Record<string, unknown> | null>(null);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    const res = await resumeApi.upload(file);
    setResumeId(res.resume_id || res.id);
    setUploading(false);
  };

  const handleAnalyze = async () => {
    const res = await invoke({
      message: "帮我解析简历",
      resume_path: "D:/project/JobPilot-AI/uploads/zhangsan.docx",
      thread_id: "resume_" + Date.now(),
      resume_id: resumeId,
      approved: false,
    });
    if (res?.resume_json) setParsed(res.resume_json as Record<string, unknown>);
  };

  return (
    <div className="space-y-6 max-w-4xl">
      <h1 className="text-2xl font-bold text-gray-900">简历中心</h1>

      {/* Upload */}
      <div className="bg-white rounded-xl border border-gray-100 p-6">
        <h3 className="text-sm font-semibold text-gray-900 mb-4">上传简历</h3>
        <label className="flex items-center gap-3 px-4 py-3 border-2 border-dashed border-gray-200 rounded-xl cursor-pointer hover:border-gray-400 transition-colors">
          <Upload size={20} className="text-gray-400" />
          <span className="text-sm text-gray-600">{uploading ? "上传中..." : "点击上传 PDF/DOCX"}</span>
          <input type="file" accept=".pdf,.docx" onChange={handleUpload} className="hidden" />
        </label>
      </div>

      {/* Workflow */}
      <WorkflowTimeline plan={plan} />

      {/* Analyze */}
      <button onClick={handleAnalyze} disabled={loading}
        className="px-4 py-2.5 bg-gray-900 text-white rounded-lg text-sm font-medium disabled:opacity-50 flex items-center gap-2">
        {loading ? <Loader2 size={16} className="animate-spin" /> : <FileText size={16} />}
        {loading ? "解析中..." : "解析简历"}
      </button>

      {/* Result */}
      {parsed && (
        <div className="bg-white rounded-xl border border-gray-100 p-4">
          <pre className="text-xs text-gray-600 overflow-auto max-h-80">{JSON.stringify(parsed, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
