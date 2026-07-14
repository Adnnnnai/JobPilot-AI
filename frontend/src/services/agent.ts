import api from "@/lib/axios";

export const agentApi = {
  workflow: (data: Record<string, unknown>) =>
    api.post("/agent/workflow", data),
  approve: (threadId: string, resumeId: number) =>
    api.post("/agent/workflow/approve", { thread_id: threadId, resume_id: resumeId }),
};
