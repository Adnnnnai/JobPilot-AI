import { create } from "zustand";
import type { TaskPlan, InterviewQuestion } from "@/types/agent";

interface WorkflowState {
  plan: TaskPlan[];
  currentAgent: string;
  rewriteResult: string;
  rewritePlan: Record<string, unknown>;
  questions: InterviewQuestion[];
  loading: boolean;

  setPlan: (plan: Record<string, unknown>[]) => void;
  setCurrentAgent: (agent: string) => void;
  setRewriteResult: (result: string) => void;
  setRewritePlan: (plan: Record<string, unknown>) => void;
  setQuestions: (q: Record<string, unknown>[]) => void;
  setLoading: (v: boolean) => void;
  reset: () => void;
}

export const useWorkflowStore = create<WorkflowState>((set) => ({
  plan: [],
  currentAgent: "",
  rewriteResult: "",
  rewritePlan: {},
  questions: [],
  loading: false,

  setPlan: (plan) => set({ plan: plan.map((p, i) => ({
    id: (p.id as number) ?? i,
    name: (p.name as string) ?? "",
    description: (p.description as string) ?? "",
    agent: (p.agent as string) ?? "",
    depends: (p.depends as number[]) ?? [],
    status: (p.status as TaskPlan["status"]) ?? "pending",
  })) }),
  setCurrentAgent: (agent) => set({ currentAgent: agent }),
  setRewriteResult: (result) => set({ rewriteResult: result }),
  setRewritePlan: (plan) => set({ rewritePlan: plan }),
  setQuestions: (q) => set({ questions: q.map((item) => ({
    category: (item.category as string) ?? "",
    question: (item.question as string) ?? "",
  })) }),
  setLoading: (v) => set({ loading: v }),
  reset: () => set({ plan: [], currentAgent: "", rewriteResult: "", rewritePlan: {}, questions: [], loading: false }),
}));
