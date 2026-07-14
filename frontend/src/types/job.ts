export interface JobDescription {
  id?: number;
  title: string;
  company: string;
  salary: string;
  city: string;
  tech_stack: string;
  requirements: string;
  description: string;
  source: string;
}

export interface MatchResult {
  score?: number;
  analysis?: string;
}
