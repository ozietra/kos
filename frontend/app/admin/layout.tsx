'use client'

import { useEffect, useState } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import { auth } from '@/lib/api'

const NAV = [
  { href: '/admin', label: 'Genel Bakış' },
  { href: '/admin/programlar', label: 'Program Güncellemeleri' },
  { href: '/admin/fiyatlandirma', label: 'Fiyatlandırma' },
  { href: '/admin/icerik', label: 'Site İçeriği' },
]

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter()
  const pathname = usePathname()
  const [state, setState] = useState<'loading' | 'ok' | 'denied'>('loading')

  useEffect(() => {
    auth
      .me()
      .then((u) => setState(u.is_admin ? 'ok' : 'denied'))
      .catch(() => router.replace('/giris?next=/admin'))
  }, [router])

  if (state === 'loading') {
    return <div style={{ padding: 48, textAlign: 'center', color: '#666' }}>Yükleniyor…</div>
  }
  if (state === 'denied') {
    return (
      <div style={{ padding: 48, textAlign: 'center' }}>
        <h2>Erişim yetkiniz yok</h2>
        <p style={{ color: '#666', marginTop: 8 }}>Bu alana yalnızca yöneticiler girebilir.</p>
        <a href="/dashboard" style={{ color: '#003366' }}>Panele dön</a>
      </div>
    )
  }

  return (
    <div style={{ maxWidth: 1100, margin: '0 auto', padding: '24px 20px' }}>
      <h1 style={{ fontSize: 24, fontWeight: 700, marginBottom: 16 }}>Yönetim Paneli</h1>
      <nav style={{ display: 'flex', gap: 8, flexWrap: 'wrap', borderBottom: '1px solid #e4e3dc', marginBottom: 24, paddingBottom: 12 }}>
        {NAV.map((n) => (
          <a
            key={n.href}
            href={n.href}
            style={{
              padding: '8px 14px',
              borderRadius: 6,
              fontSize: 14,
              fontWeight: 600,
              textDecoration: 'none',
              color: pathname === n.href ? '#fff' : '#003366',
              background: pathname === n.href ? '#003366' : '#f4f3ee',
            }}
          >
            {n.label}
          </a>
        ))}
      </nav>
      {children}
    </div>
  )
}
