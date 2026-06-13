'use client'

import { useEffect, useState } from 'react'
import { admin } from '@/lib/api'

export default function AdminDashboard() {
  const [stats, setStats] = useState<any>(null)
  const [err, setErr] = useState('')

  useEffect(() => {
    admin.stats().then(setStats).catch((e) => setErr(e.message))
  }, [])

  const cards = stats
    ? [
        { label: 'Toplam Kullanıcı', value: stats.user_count },
        { label: 'Toplam Başvuru', value: stats.application_count },
        { label: 'Ödeme Sayısı', value: stats.paid_count },
        { label: 'Toplam Gelir', value: `${(stats.total_revenue_try || 0).toLocaleString('tr-TR')} ₺` },
      ]
    : []

  return (
    <div>
      {err && <p style={{ color: '#c0392b' }}>{err}</p>}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(200px,1fr))', gap: 16 }}>
        {cards.map((c) => (
          <div key={c.label} style={{ border: '1px solid #e4e3dc', borderRadius: 8, padding: 20 }}>
            <div style={{ fontSize: 28, fontWeight: 700, color: '#003366' }}>{c.value ?? '—'}</div>
            <div style={{ color: '#6b6a62', fontSize: 14, marginTop: 4 }}>{c.label}</div>
          </div>
        ))}
      </div>
      <p style={{ marginTop: 24, color: '#6b6a62', fontSize: 14 }}>
        Soldaki menüden program güncellemelerini onaylayabilir, fiyatları ve site içeriğini düzenleyebilirsiniz.
      </p>
    </div>
  )
}
