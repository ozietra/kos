'use client'

import { useEffect, useState } from 'react'
import { admin } from '@/lib/api'

export default function AdminPricingPage() {
  const [plans, setPlans] = useState<any[]>([])
  const [msg, setMsg] = useState('')
  const [saving, setSaving] = useState<string | null>(null)

  const load = () => admin.pricing().then(setPlans).catch((e) => setMsg(e.message))
  useEffect(() => { load() }, [])

  const set = (code: string, field: string, value: any) =>
    setPlans((ps) => ps.map((p) => (p.code === code ? { ...p, [field]: value } : p)))

  const save = async (p: any) => {
    setSaving(p.code)
    try {
      await admin.updatePricing(p.code, {
        name: p.name,
        description: p.description,
        price_try: parseFloat(p.price_try) || 0,
        campaign_price_try: p.campaign_price_try === '' || p.campaign_price_try == null ? null : parseFloat(p.campaign_price_try),
        clear_campaign: !p.campaign_price_try,
        campaign_label: p.campaign_label || null,
        campaign_start: p.campaign_start || null,
        campaign_end: p.campaign_end || null,
        is_active: p.is_active,
      })
      setMsg('Kaydedildi: ' + p.name)
      load()
    } catch (e: any) {
      setMsg(e.message)
    } finally {
      setSaving(null)
    }
  }

  const inp = { padding: '8px 10px', border: '1px solid #d8d8d8', borderRadius: 6, width: '100%' } as const
  const row = { display: 'flex', gap: 10, alignItems: 'center', marginBottom: 8 } as const
  const lbl = { flex: '0 0 160px', fontSize: 13, color: '#6b6a62' } as const

  return (
    <div>
      <p style={{ color: '#6b6a62', fontSize: 14, marginBottom: 16 }}>
        Fiyatları TL olarak girin. Kampanya fiyatı girip tarih aralığı belirlerseniz, o aralıkta indirimli fiyat sitede otomatik gösterilir.
        Kampanyayı kaldırmak için kampanya fiyatını boş bırakın.
      </p>
      {msg && <div style={{ background: '#f4f3ee', padding: 10, borderRadius: 6, marginBottom: 16, fontSize: 14 }}>{msg}</div>}
      {plans.map((p) => (
        <div key={p.code} style={{ border: '1px solid #e4e3dc', borderRadius: 8, padding: 16, marginBottom: 16 }}>
          <h3 style={{ marginBottom: 12 }}>{p.name} <span style={{ color: '#a8a79f', fontWeight: 400 }}>({p.code})</span></h3>
          <div style={row}><span style={lbl}>Plan adı</span><input style={inp} value={p.name || ''} onChange={(e) => set(p.code, 'name', e.target.value)} /></div>
          <div style={row}><span style={lbl}>Açıklama</span><input style={inp} value={p.description || ''} onChange={(e) => set(p.code, 'description', e.target.value)} /></div>
          <div style={row}><span style={lbl}>Normal fiyat (₺)</span><input type="number" style={inp} value={p.price_try ?? ''} onChange={(e) => set(p.code, 'price_try', e.target.value)} /></div>
          <hr style={{ border: 0, borderTop: '1px dashed #e4e3dc', margin: '12px 0' }} />
          <div style={row}><span style={lbl}>Kampanya fiyatı (₺)</span><input type="number" placeholder="boş = kampanya yok" style={inp} value={p.campaign_price_try ?? ''} onChange={(e) => set(p.code, 'campaign_price_try', e.target.value)} /></div>
          <div style={row}><span style={lbl}>Kampanya etiketi</span><input style={inp} placeholder="örn. Yıl sonu indirimi" value={p.campaign_label || ''} onChange={(e) => set(p.code, 'campaign_label', e.target.value)} /></div>
          <div style={row}><span style={lbl}>Kampanya başlangıç</span><input type="date" style={inp} value={p.campaign_start || ''} onChange={(e) => set(p.code, 'campaign_start', e.target.value)} /></div>
          <div style={row}><span style={lbl}>Kampanya bitiş</span><input type="date" style={inp} value={p.campaign_end || ''} onChange={(e) => set(p.code, 'campaign_end', e.target.value)} /></div>
          <div style={row}><span style={lbl}>Aktif</span><input type="checkbox" checked={!!p.is_active} onChange={(e) => set(p.code, 'is_active', e.target.checked)} /></div>
          <button onClick={() => save(p)} disabled={saving === p.code} style={{ marginTop: 8, background: '#003366', color: '#fff', border: 0, borderRadius: 6, padding: '10px 18px', fontWeight: 600, cursor: 'pointer' }}>
            {saving === p.code ? 'Kaydediliyor…' : 'Kaydet'}
          </button>
        </div>
      ))}
    </div>
  )
}
