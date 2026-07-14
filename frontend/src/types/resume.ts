export interface Resume {
  id: number;
  filename: string;
  status: string;
  filepath: string;
  created_at?: string;
}

export interface ResumeJSON {
  name: string;
  phone: string;
  email: string;
  education: Education[];
  skills: string[];
  projects: Project[];
}

export interface Education {
  school?: string;
  institution?: string;
  major: string;
  degree?: string;
  start?: string;
  end?: string;
}

export interface Project {
  title: string;
  description: string;
  role?: string;
}
