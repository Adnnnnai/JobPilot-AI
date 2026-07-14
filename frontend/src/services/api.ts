import api from "@/lib/axios";

export const authApi = {
  login: (email: string, password: string) =>
    api.post("/auth/login", { email, password }),
  register: (username: string, email: string, password: string) =>
    api.post("/auth/register", { username, email, password }),
};

export const resumeApi = {
  upload: (file: File) => {
    const fd = new FormData();
    fd.append("file", file);
    return api.post("/resume/upload", fd, {
      headers: { "Content-Type": "multipart/form-data" },
    }).then(res => res.data);
  },
  analyze: (resumeId: number) =>
    api.post("/resume/analyze", { resume_id: resumeId }).then(res => res.data),
};

export const agentApi = {
  workflow: (data: Record<string, unknown>) =>
    api.post("/agent/workflow", data).then(res => res.data),
  approve: (threadId: string, resumeId: number) =>
    api.post("/agent/workflow/approve", { thread_id: threadId, resume_id: resumeId }),
};
