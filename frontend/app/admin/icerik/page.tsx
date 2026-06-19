'use client'

import { useEffect, useState } from 'react'
import { admin } from '@/lib/api'

export default function AdminContentPage() {
  const [items, setItems] = useState<any[]>([])
  const [msg, setMsg] = useState('')
  const [saving, setSaving] = useState<string | null>(null)

  useEffect(() => {
    admin.content().then(setItems).catch((e) => setMsg(e.message))
  }, [])

  const save = async (key: string, value: string) => {
    setSaving(key)
    try {
      await admin.updateContent(key, { value })
      setMsg('Kaydedildi: ' + key)
    } catch (e: any) {
      setMsg(e.message)
    } finally {
      setSaving(null)
    }
  }

  return (
    <div>
      <p style={{ color: '#6b6a62', fontSize: 14, marginBottom: 16 }}>
        Ana sayfa istatistikleri, hero rozeti ve <strong>Google Analytics / Search Console</strong> kimlikleri.
        Hero rozetini boş bırakırsanız en yakın program son başvuru tarihinden otomatik üretilir.
        Analytics ölçüm kimliğini (G-…) veya Search Console doğrulama kodunu girip kaydederseniz site otomatik olarak bağlanır.
        Değişiklikler kısa süre içinde siteye yansır (gerekirse tarayıcı önbelleğini yenileyin).
      </p>
      {msg && <div style={{ background: '#f4f3ee', padding: 10, borderRadius: 6, marginBottom: 16, fontSize: 14 }}>{msg}</div>}
      {items.map((it) => (
        <div key={it.key} style={{ display: 'flex', gap: 12, alignItems: 'center', marginBottom: 10 }}>
          <label style={{ flex: '0 0 320px', fontSize: 14, color: '#1a1a18' }}>{it.label || it.key}</label>
          <input
            defaultValue={it.value || ''}
            onChange={(e) => (it.value = e.target.value)}
            style={{ flex: 1, padding: '8px 10px', border: '1px solid #d8d8d8', borderRadius: 6 }}
          />
          <button
            onClick={() => save(it.key, it.value || '')}
            disabled={saving === it.key}
            style={{ background: '#003366', color: '#fff', border: 0, borderRadius: 6, padding: '8px 14px', cursor: 'pointer' }}
          >
            {saving === it.key ? '…' : 'Kaydet'}
          </button>
        </div>
      ))}
    </div>
  )
}
