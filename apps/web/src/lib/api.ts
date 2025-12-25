const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface FetchOptions extends RequestInit {
  token?: string;
}

async function fetchApi<T>(
  endpoint: string,
  options: FetchOptions = {}
): Promise<T> {
  const { token, ...fetchOptions } = options;

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  if (token) {
    (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...fetchOptions,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `API Error: ${response.status}`);
  }

  return response.json();
}

// Exercise API
export const exerciseApi = {
  list: (token: string) =>
    fetchApi<{ exercises: Exercise[] }>("/api/v1/exercises", { token }),

  get: (id: string, token: string) =>
    fetchApi<Exercise>(`/api/v1/exercises/${id}`, { token }),

  create: (data: ExerciseFormData, token: string) =>
    fetchApi<Exercise>("/api/v1/exercises", {
      method: "POST",
      body: JSON.stringify(data),
      token,
    }),

  update: (id: string, data: Partial<ExerciseFormData>, token: string) =>
    fetchApi<Exercise>(`/api/v1/exercises/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
      token,
    }),

  delete: (id: string, token: string) =>
    fetchApi<void>(`/api/v1/exercises/${id}`, {
      method: "DELETE",
      token,
    }),
};

// Client API
export const clientApi = {
  list: (token: string) =>
    fetchApi<{ clients: Client[] }>("/api/v1/clients", { token }),

  get: (id: string, token: string) =>
    fetchApi<Client>(`/api/v1/clients/${id}`, { token }),

  create: (data: Partial<Client>, token: string) =>
    fetchApi<Client>("/api/v1/clients", {
      method: "POST",
      body: JSON.stringify(data),
      token,
    }),
};

// Assessment API
export const assessmentApi = {
  list: (clientId: string, token: string) =>
    fetchApi<{ assessments: Assessment[] }>(
      `/api/v1/clients/${clientId}/assessments`,
      { token }
    ),

  get: (clientId: string, assessmentId: string, token: string) =>
    fetchApi<Assessment>(
      `/api/v1/clients/${clientId}/assessments/${assessmentId}`,
      { token }
    ),

  create: (clientId: string, data: Partial<Assessment>, token: string) =>
    fetchApi<Assessment>(`/api/v1/clients/${clientId}/assessments`, {
      method: "POST",
      body: JSON.stringify(data),
      token,
    }),

  generatePlan: (
    clientId: string,
    assessmentId: string,
    preferences: CoachPreferences,
    token: string
  ) =>
    fetchApi<{ plan: WorkoutPlan; message: string }>(
      `/api/v1/clients/${clientId}/assessments/${assessmentId}/generate-plan`,
      {
        method: "POST",
        body: JSON.stringify(preferences),
        token,
      }
    ),
};

// Workout Plan API
export const planApi = {
  list: (token: string) =>
    fetchApi<{ plans: WorkoutPlan[] }>("/api/v1/plans", { token }),

  get: (id: string, token: string) =>
    fetchApi<{ plan: WorkoutPlan; days: WorkoutDay[] }>(`/api/v1/plans/${id}`, {
      token,
    }),

  sendEmail: (id: string, token: string) =>
    fetchApi<{ message: string }>(`/api/v1/plans/${id}/send-email`, {
      method: "POST",
      token,
    }),
};

// Import types
import type {
  Exercise,
  ExerciseFormData,
  Client,
  Assessment,
  WorkoutPlan,
  WorkoutDay,
  CoachPreferences,
} from "@/types";
