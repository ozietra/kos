/**
 * API Client — backend FastAPI'ye istek gönderir
 * Next.js rewrite kuralı sayesinde /api/* → backend:8000/api/*
 */

const API_BASE = '/api'

function getAuthHeader(): Record<string, string> {
  if (typeof window === 'undefined') return {}
  const token = localStorage.getItem('token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeader(),
      ...(options.headers || {}),
    },
    ...options,
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Bir hata oluştu.' }))
    throw new Error(err.detail || `HTTP ${res.status}`)
  }

  if (res.status === 204) return undefined as T
  return res.json()
}

// ── Auth ──────────────────────────────────────────────────────────────────────
export const auth = {
  register: (email: string, password: string, name?: string) =>
    request<{ id: string; email: string }>('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password, name }),
    }),

  login: (email: string, password: string) =>
    request<{ access_token: string }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }),

  me: () => request<{ id: string; email: string; name: string; plan: string; is_admin: boolean }>('/auth/me'),

  forgotPassword: (email: string) =>
    request('/auth/forgot-password', { method: 'POST', body: JSON.stringify({ email }) }),

  resetPassword: (token: string, new_password: string) =>
    request('/auth/reset-password', { method: 'POST', body: JSON.stringify({ token, new_password }) }),
}

// ── Businesses ────────────────────────────────────────────────────────────────
export const businesses = {
  list: () => request<any[]>('/businesses'),
  create: (data: any) => request<any>('/businesses', { method: 'POST', body: JSON.stringify(data) }),
  get: (id: string) => request<any>(`/businesses/${id}`),
  update: (id: string, data: any) => request<any>(`/businesses/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id: string) => request<void>(`/businesses/${id}`, { method: 'DELETE' }),
}

// ── Eligibility ───────────────────────────────────────────────────────────────
export const eligibility = {
  check: (business_id: string) =>
    request<any>(`/eligibility/check?business_id=${business_id}`, { method: 'POST' }),
  getLast: (business_id: string) =>
    request<any>(`/eligibility/${business_id}`),
}

// ── NACE ─────────────────────────────────────────────────────────────────────
export const nace = {
  suggest: (description: string) =>
    request<any>('/nace/suggest', { method: 'POST', body: JSON.stringify({ description }) }),
  search: (q: string) =>
    request<any[]>(`/nace/search?q=${encodeURIComponent(q)}`),
}

// ── Programs ─────────────────────────────────────────────────────────────────
export const programs = {
  list: () => request<any[]>('/programs'),
  get: (id: string) => request<any>(`/programs/${id}`),
}

// ── Applications ─────────────────────────────────────────────────────────────
export const applications = {
  create: (data: any) =>
    request<any>('/applications', { method: 'POST', body: JSON.stringify(data) }),
  get: (id: string) => request<any>(`/applications/${id}`),
  saveInputs: (id: string, data: any) =>
    request<any>(`/applications/${id}/inputs`, { method: 'PUT', body: JSON.stringify(data) }),
  startGeneration: (id: string) =>
    request<any>(`/applications/${id}/generate`, { method: 'POST' }),
  getDocuments: (id: string) => request<any[]>(`/applications/${id}/documents`),
  getProgressUrl: (id: string) => `${API_BASE}/applications/${id}/progress`,
  getPdfUrl: (id: string) => `${API_BASE}/applications/${id}/pdf`,
}

// ── Public içerik (kimlik gerektirmez) ──────────────────────────────────────
export const content = {
  home: () => request<{ hero_badge: string; stats: any[] }>('/content/home'),
  pricing: () => request<{ plans: any[] }>('/content/pricing'),
}

// ── Token helpers ─────────────────────────────────────────────────────────────
export const tokenHelpers = {
  save: (token: string) => localStorage.setItem('token', token),
  remove: () => localStorage.removeItem('token'),
  get: () => localStorage.getItem('token'),
}

// ── Payments ──────────────────────────────────────────────────────────────────
export const payments = {
  checkout: (data: { application_id: string; plan: string; provider?: string }) =>
    request<{ provider?: string; checkoutFormContent?: string; paymentPageUrl?: string; token?: string; iframe_url?: string }>(
      '/payments/checkout',
      { method: 'POST', body: JSON.stringify(data) }
    ),

  result: (token: string) =>
    request<{ status: string; plan: string }>(`/payments/result?token=${encodeURIComponent(token)}`),

  myPayments: () => request<any[]>('/payments/my'),
}

// ── Admin ─────────────────────────────────────────────────────────────────────
export const admin = {
  stats: () => request<any>('/admin/stats'),
  users: (skip = 0, limit = 50) => request<any[]>(`/admin/users?skip=${skip}&limit=${limit}`),
  adminPayments: (skip = 0, limit = 50) => request<any[]>(`/admin/payments?skip=${skip}&limit=${limit}`),
  updateProgram: (id: string, data: any) =>
    request<any>(`/admin/programs/${id}`, { method: 'PUT', body: JSON.stringify(data) }),

  // Program oto-güncelleme önerileri
  proposals: (status = 'pending') =>
    request<any[]>(`/admin/programs/proposals?status_filter=${encodeURIComponent(status)}`),
  approveProposal: (id: string) =>
    request<any>(`/admin/programs/proposals/${id}/approve`, { method: 'POST' }),
  rejectProposal: (id: string, note?: string) =>
    request<any>(`/admin/programs/proposals/${id}/reject`, { method: 'POST', body: JSON.stringify({ note }) }),
  refreshPrograms: () => request<any>('/admin/programs/refresh', { method: 'POST' }),

  // Site içeriği
  content: () => request<any[]>('/admin/content'),
  updateContent: (key: string, data: { value?: string; label?: string }) =>
    request<any>(`/admin/content/${encodeURIComponent(key)}`, { method: 'PUT', body: JSON.stringify(data) }),

  // Fiyatlandırma
  pricing: () => request<any[]>('/admin/pricing'),
  updatePricing: (code: string, data: any) =>
    request<any>(`/admin/pricing/${encodeURIComponent(code)}`, { method: 'PUT', body: JSON.stringify(data) }),
}
