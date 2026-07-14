"use client";

import { useState } from "react";
import { useAgent } from "@/hooks/useAgent";
import { WorkflowTimeline } from "@/components/WorkflowTimeline";
import { Mic, Loader2 } from "lucide-react";

export default function InterviewPage() {
  const { loading, plan, invoke } = useAgent();
  const [jd, setJd] = useState("AI Agent开发工程师");
  const [questions, setQuestions] = useState<{ category: string; question: string }[]>([]);
  const [answers, setAnswers] = useState<Record<number, string>>({});

  const handleGenerate = async () => {
    const res = await invoke({
      message: "帮我生成面试题",
      resume_path: "D:/project/JobPilot-AI/uploads/zhangsan.docx",
      jd, thread_id: "interview_" + Date.now(), resume_id: 8, approved: false,
    });
    if (res?.interview_questions?.length > 0) {
      setQuestions(res.interview_questions);
    }
  };

  return (
    <div className="space-y-6 max-w-3xl">
      <h1 className="text-2xl font-bold text-gray-900">模拟面试</h1>
      <div className="bg-white rounded-xl border border-gray-100 p-4 flex gap-3">
        <div className="flex-1">
          <label className="text-xs font-medium text-gray-500">目标岗位</label>
          <input value={jd} onChange={e => setJd(e.target.value)}
            className="mt-1 w-full px-3 py-2 bg-gray-50 rounded-lg text-sm outline-none" />
        </div>
        <button onClick={handleGenerate} disabled={loading}
          className="px-4 py-2 bg-gray-900 text-white rounded-lg text-sm font-medium self-end disabled:opacity-50 flex items-center gap-2">
          {loading ? <Loader2 size={16} className="animate-spin" /> : <Mic size={16} />}
          生成题目
        </button>
      </div>
      <WorkflowTimeline plan={plan} />
      {questions.length > 0 && (
        <div className="space-y-4">
          {questions.map((q, i) => (
            <div key={i} className="bg-white rounded-xl border border-gray-100 p-5">
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-xs font-medium text-gray-400 bg-gray-50 px-2 py-0.5 rounded">{q.category}</span>
                  <p className="text-sm text-gray-800 mt-2 font-medium">Q{i + 1}. {q.question}</p>
                </div>
                <span className="text-xs text-gray-300">#{i + 1}</span>
              </div>
              <textarea
                value={answers[i] || ""}
                onChange={e => setAnswers(prev => ({ ...prev, [i]: e.target.value }))}
                placeholder="请输入你的回答..."
                className="mt-3 w-full px-3 py-2 bg-gray-50 rounded-lg text-sm outline-none resize-none h-20"
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
