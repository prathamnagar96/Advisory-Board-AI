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

export type DocumentItem = {
    id: string;
    filename: string;
    file_type: string;
    size: number;
    processed: boolean;
    upload_timestamp: string;
};

export type DashboardFinancialOverview = {
    total_income: number;
    total_deductions: number;
    tax_liability: number;
    net_income: number;
    assessment_year: string;
};

export type DashboardQuickStats = {
    documents_uploaded: number;
    queries_asked: number;
    reminders_pending: number;
    tax_savings_estimate: number;
};

export type DashboardActivity = {
    id: string;
    type: 'query' | 'document' | 'reminder';
    title: string;
    timestamp: string;
    metadata?: Record<string, unknown>;
};

export type DashboardReminder = {
    id: string;
    title: string;
    description?: string;
    due_date: string;
    priority: 'low' | 'medium' | 'high';
    type: string;
};

export type DashboardOverview = {
    financial_overview: DashboardFinancialOverview;
    quick_stats: DashboardQuickStats;
    recent_activities?: DashboardActivity[];
    upcoming_reminders?: DashboardReminder[];
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
    return apiFetch<DashboardOverview>(`/api/dashboard/overview`);
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
    return apiFetch<{ documents: DocumentItem[] }>(`/api/documents`);
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
