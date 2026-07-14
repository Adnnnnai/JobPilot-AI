"use client";

import { useState, useCallback } from "react";
import { agentApi } from "@/services/api";

interface TaskPlan {
  id: number;
  name: string;
  description: string;
  agent: string;
  status: string;
  depends: number[];
}

function normalizeTask(t: Record<string, unknown>): TaskPlan {
  return {
    id: (t.id as number) ?? 0,
    name: (t.name as string) ?? "",
    description: (t.description as string) ?? "",
    agent: (t.agent as string) ?? "",
    status: (t.status as string) ?? "pending",
    depends: (t.depends as number[]) ?? [],
  };
}

export function useAgent() {
  const [loading, setLoading] = useState(false);
  const [plan, setPlan] = useState<TaskPlan[]>([]);
  const [result, setResult] = useState("");
  const [rewritePlan, setRewritePlan] = useState<Record<string, unknown>>({});
  const [questions, setQuestions] = useState<{ category: string; question: string }[]>([]);

  const invoke = useCallback(async (data: Record<string, unknown>) => {
    setLoading(true);
    try {
      const r = await agentApi.workflow(data);
      // Update states from response
      const taskPlan = (r.task_plan || []).map(normalizeTask);
      setPlan(taskPlan);
      setResult(r.rewrite_result || "");
      setRewritePlan(r.rewrite_plan || {});
      setQuestions((r.interview_questions || []).map((q: Record<string, unknown>) => ({
        category: (q.category as string) ?? "",
        question: (q.question as string) ?? "",
      })));
      return r;
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail
        || (err as Error)?.message
        || "Unknown error";
      setResult(`Error: ${msg}`);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  return { loading, plan, result, rewritePlan, questions, invoke, setPlan, setResult };
}
