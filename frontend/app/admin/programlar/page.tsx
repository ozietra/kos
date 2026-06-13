'use client'

import { useEffect, useState } from 'react'
import { admin } from '@/lib/api'

export default function AdminProgramsPage() {
  const [proposals, setProposals] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [busy, setBusy] = useState(false)
  const [msg, setMsg] = useState('')

  const load = () => {
    setLoading(true)
    admin
      .proposals('pending')
      .then(setProposals)
      .catch((e) => setMsg(e.message))
      .finally(() => setLoading(false))
  }

  useEffect(load, [])

  const refresh = async () => {
    setBusy(true)
    setMsg('KOSGEB sitesinden güncel veriler çekiliyor…')
    try {
      const r = await admin.refreshPrograms()
      setMsg(`Tarama bitti: ${r.total_proposals} yeni öneri oluştu.`)
      load()
    } catch (e: any) {
      setMsg('Tarama hatası: ' + e.message)
    } finally {
      setBusy(false)
    }
  }

  const decide = async (id: string, approve: boolean) => {
    try {
      if (approve) await admin.approveProposal(id)
      else await admin.rejectProposal(id)
      setProposals((p) => p.filter((x) => x.id !== id))
    } catch (e: any) {
      setMsg(e.message)
    }
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <p style={{ color: '#6b6a62', fontSize: 14 }}>
          Onay bekleyen değişiklikler. Onayladıklarınız anında sitedeki programlara yansır.
        </p>
        <button
          onClick={refresh}
          disabled={busy}
          style={{ background: '#003366', color: '#fff', border: 0, borderRadius: 6, padding: '10px 16px', fontWeight: 600, cursor: 'pointer' }}
        >
          {busy ? 'Çekiliyor…' : 'Şimdi Güncelle'}
        </button>
      </div>

      {msg && <div style={{ background: '#f4f3ee', padding: 12, borderRadius: 6, marginBottom: 16, fontSize: 14 }}>{msg}</div>}

      {loading ? (
        <p>Yükleniyor…</p>
      ) : proposals.length === 0 ? (
        <p style={{ color: '#6b6a62' }}>Bekleyen öneri yok. "Şimdi Güncelle" ile KOSGEB sitesinden kontrol edebilirsiniz.</p>
      ) : (
        proposals.map((p) => (
          <div key={p.id} style={{ border: '1px solid #e4e3dc', borderRadius: 8, padding: 16, marginBottom: 12 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <strong>{p.proposed_data?.program_name || p.program_code}</strong>
                <span style={{ marginLeft: 8, fontSize: 12, padding: '2px 8px', borderRadius: 4, background: p.change_type === 'create' ? '#1e8449' : '#d68910', color: '#fff' }}>
                  {p.change_type === 'create' ? 'YENİ PROGRAM' : 'GÜNCELLEME'}
                </span>
              </div>
              <div style={{ display: 'flex', gap: 8 }}>
                <button onClick={() => decide(p.id, true)} style={{ background: '#1e8449', color: '#fff', border: 0, borderRadius: 6, padding: '8px 14px', cursor: 'pointer' }}>Onayla</button>
                <button onClick={() => decide(p.id, false)} style={{ background: '#fff', color: '#c0392b', border: '1px solid #c0392b', borderRadius: 6, padding: '8px 14px', cursor: 'pointer' }}>Reddet</button>
              </div>
            </div>
            {p.diff_summary?.changes?.length > 0 && (
              <table style={{ width: '100%', marginTop: 12, fontSize: 13, borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ textAlign: 'left', color: '#6b6a62' }}>
                    <th style={{ padding: '4px 8px' }}>Alan</th>
                    <th style={{ padding: '4px 8px' }}>Mevcut</th>
                    <th style={{ padding: '4px 8px' }}>Önerilen</th>
                  </tr>
                </thead>
                <tbody>
                  {p.diff_summary.changes.map((c: any, i: number) => (
                    <tr key={i} style={{ borderTop: '1px solid #eee' }}>
                      <td style={{ padding: '4px 8px', fontWeight: 600 }}>{c.field}</td>
                      <td style={{ padding: '4px 8px', color: '#999' }}>{JSON.stringify(c.old)}</td>
                      <td style={{ padding: '4px 8px', color: '#1a1a18' }}>{JSON.stringify(c.new)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
            {p.source_url && (
              <div style={{ marginTop: 8, fontSize: 12, color: '#a8a79f' }}>Kaynak: {p.source_url} · Güven: {p.confidence}</div>
            )}
          </div>
        ))
      )}
    </div>
  )
}
