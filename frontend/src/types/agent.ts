export interface TaskPlan {
  id: number;
  name: string;
  description: string;
  agent: string;
  depends: number[];
  status: "pending" | "running" | "done" | "failed";
}

export interface WorkflowState {
  message: string;
  task_plan: TaskPlan[];
  current_agent: string;
  resume_json: Record<string, unknown>;
  match_result: Record<string, unknown>;
  rewrite_plan: Record<string, unknown>;
  rewrite_result: string;
  interview_questions: InterviewQuestion[];
  approved: boolean;
}

export interface InterviewQuestion {
  category: string;
  question: string;
}

export interface AgentEvent {
  node: string;
  status: "started" | "finished" | "failed";
  detail: Record<string, unknown>;
  ts: string;
}
