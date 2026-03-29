export const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const TOKEN_KEY = 'advisory_token';

export const getToken = () =>
    typeof window !== 'undefined' ? localStorage.getItem(TOKEN_KEY) : null;

export const setToken = (token: string) => {
    if (typeof window !== 'undefined') {
        localStorage.setItem(TOKEN_KEY, token);
    }
};

export const clearToken = () => {
    if (typeof window !== 'undefined') {
        localStorage.removeItem(TOKEN_KEY);
    }
};

export type Reminder = {
    id: string;
    title: string;
    description?: string;
    reminder_type: string;
    due_date: string;
    priority: string;
    is_completed: boolean;
};

async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
    const token = getToken();
    const headers = new Headers(init.headers);
    headers.set('Content-Type', 'application/json');
    if (token) headers.set('Authorization', `Bearer ${token}`);

    const res = await fetch(`${API_BASE}${path}`, { ...init, headers });
    if (!res.ok) {
        const text = await res.text();
        throw new Error(text || `Request failed with ${res.status}`);
    }
    return res.json();
}

export async function login(username: string, password: string) {
    const data = await apiFetch<{ access_token: string }>(`/api/auth/login`, {
        method: 'POST',
        body: JSON.stringify({ username, password }),
    });
    setToken(data.access_token);
    return data.access_token;
}

export async function registerUser(payload: {
    email: string;
    username: string;
    password: string;
    full_name?: string;
}) {
    return apiFetch(`/api/auth/register`, {
        method: 'POST',
        body: JSON.stringify(payload),
    });
}

export async function fetchMe() {
    return apiFetch(`/api/auth/me`);
}

export async function fetchDashboard() {
    return apiFetch(`/api/dashboard/overview`);
}

export async function fetchHealthScore() {
    return apiFetch(`/api/dashboard/financial-health-score`);
}

export async function askTaxQuestion(query: string) {
    return apiFetch(`/api/tax/query`, {
        method: 'POST',
        body: JSON.stringify({ query }),
    });
}

export async function fetchDocuments() {
    return apiFetch(`/api/documents`);
}

export async function uploadDocument(file: File) {
    const token = getToken();
    const form = new FormData();
    form.append('file', file);

    const res = await fetch(`${API_BASE}/api/documents/upload`, {
        method: 'POST',
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
        body: form,
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
}

export async function deleteDocument(id: string) {
    return apiFetch(`/api/documents/${id}`, { method: 'DELETE' });
}

export async function fetchReminders() {
    return apiFetch<{ reminders: Reminder[] }>(`/api/reminders`);
}

export async function createReminder(payload: any) {
    return apiFetch<Reminder>(`/api/reminders`, { method: 'POST', body: JSON.stringify(payload) });
}

export async function completeReminder(id: string) {
    return apiFetch<Reminder>(`/api/reminders/${id}/complete`, { method: 'POST' });
}
