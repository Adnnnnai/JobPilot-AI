"use client";

import { useState, useRef, useEffect } from "react";
import { useAgent } from "@/hooks/useAgent";
import { WorkflowTimeline } from "@/components/WorkflowTimeline";
import { Send, Loader2, Zap, Bot, User } from "lucide-react";

export default function WorkspacePage() {
  const { loading, plan, invoke } = useAgent();
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => { scrollRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMsg = input;
    setMessages(prev => [...prev, { role: "user", content: userMsg }]);
    setInput("");

    const res = await invoke({
      message: userMsg,
      resume_path: "D:/project/JobPilot-AI/uploads/zhangsan.docx",
      jd: "AI Agent开发工程师",
      thread_id: "workspace_" + Date.now(),
      resume_id: 8,
      approved: false,
    });

    // Build response from return value (not stale state)
    const parts: string[] = [];
    if (res?.task_plan?.length > 0) parts.push(`**任务计划**: ${res.task_plan.map((p: {name: string}) => p.name).join(" → ")}`);
    if (res?.rewrite_plan && Object.keys(res.rewrite_plan).length > 0) parts.push("**改写计划已生成**，点击确认执行");
    if (res?.rewrite_result) parts.push(`**改写结果**:\n${res.rewrite_result.slice(0, 800)}`);
    if (res?.match_result) {
      try {
        const m = typeof res.match_result === "string" ? JSON.parse(res.match_result) : res.match_result;
        if (m.score) parts.push(`**匹配度**: ${m.score}%`);
        if (m.summary) parts.push(`**分析**: ${m.summary}`);
        if (m.matched_skills?.length > 0) parts.push(`**匹配技能**: ${m.matched_skills.join(", ")}`);
      } catch {
        parts.push(`**结果**: ${String(res.match_result).slice(0, 300)}`);
      }
    }
    if (res?.interview_questions?.length > 0) parts.push(`**面试题**: 共 ${res.interview_questions.length} 题`);
    if (res?.resume_json && Object.keys(res.resume_json).length > 0) {
      const rj = res.resume_json as Record<string,unknown>;
      if (rj.name) parts.push(`**简历**: ${rj.name}`);
      if (rj.skills?.length > 0) parts.push(`**技能**: ${(rj.skills as string[]).join(", ")}`);
    }

    setMessages(prev => [...prev, { role: "assistant", content: parts.join("\n\n") || "Task completed." }]);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSend(); }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-7rem)] max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
        <Zap size={22} className="text-yellow-500" /> AI 工作区
      </h1>
      <WorkflowTimeline plan={plan} />
      <div className="flex-1 bg-white rounded-xl border border-gray-100 mt-4 flex flex-col">
        <div className="flex-1 overflow-auto p-4 space-y-4">
          {messages.length === 0 && (
            <div className="text-center text-gray-400 mt-20">
              <Bot size={40} className="mx-auto mb-3 opacity-30" />
              <p className="text-sm">试试: "帮我找深圳AI Agent岗位并优化简历"</p>
            </div>
          )}
          {messages.map((m, i) => (
            <div key={i} className={`flex gap-3 ${m.role === "user" ? "justify-end" : ""}`}>
              {m.role === "assistant" && <div className="w-7 h-7 rounded-full bg-gray-900 flex items-center justify-center"><Bot size={14} className="text-white" /></div>}
              <div className={`max-w-[80%] px-4 py-2.5 rounded-xl text-sm whitespace-pre-wrap ${m.role === "user" ? "bg-gray-900 text-white" : "bg-gray-50 text-gray-700"}`}>{m.content}</div>
              {m.role === "user" && <div className="w-7 h-7 rounded-full bg-blue-500 flex items-center justify-center"><User size={14} className="text-white" /></div>}
            </div>
          ))}
          {loading && (
            <div className="flex gap-3">
              <div className="w-7 h-7 rounded-full bg-gray-900 flex items-center justify-center"><Bot size={14} className="text-white" /></div>
              <div className="bg-gray-50 px-4 py-2.5 rounded-xl text-sm text-gray-400 flex items-center gap-2"><Loader2 size={14} className="animate-spin" /> Agent 工作中...</div>
            </div>
          )}
          <div ref={scrollRef} />
        </div>
        <div className="border-t border-gray-100 p-3 flex gap-3">
          <textarea value={input} onChange={e => setInput(e.target.value)} onKeyDown={handleKeyDown}
            placeholder="告诉你的 AI 助手要做什么..."
            className="flex-1 px-3 py-2 bg-gray-50 rounded-lg text-sm outline-none resize-none h-10" />
          <button onClick={handleSend} disabled={loading || !input.trim()}
            className="px-4 py-2 bg-gray-900 text-white rounded-lg text-sm font-medium disabled:opacity-40 flex items-center gap-1.5">
            <Send size={16} /> 发送
          </button>
        </div>
      </div>
    </div>
  );
}
