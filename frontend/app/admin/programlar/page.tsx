'use client'

import { useEffect, useState } from 'react'
import { admin, programs as programsApi } from '@/lib/api'

export default function AdminProgramsPage() {
  const [proposals, setProposals] = useState<any[]>([])
  const [programs, setPrograms] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [busy, setBusy] = useState(false)
  const [msg, setMsg] = useState('')
  const [savingId, setSavingId] = useState<string | null>(null)

  const load = () => {
    setLoading(true)
    admin
      .proposals('pending')
      .then(setProposals)
      .catch((e) => setMsg(e.message))
      .finally(() => setLoading(false))
  }

  const loadPrograms = () => programsApi.list().then(setPrograms).catch(() => {})

  useEffect(() => { load(); loadPrograms() }, [])

  const setProg = (id: string, field: string, value: any) =>
    setPrograms((ps) => ps.map((p) => (p.id === id ? { ...p, [field]: value } : p)))

  const saveProgram = async (p: any) => {
    setSavingId(p.id)
    try {
      await admin.updateProgram(p.id, {
        program_name: p.program_name,
        application_period_start: p.application_period_start || null,
        application_period_end: p.application_period_end || null,
        is_active: p.is_active,
      })
      setMsg(`Kaydedildi: ${p.program_name}`)
      loadPrograms()
    } catch (e: any) {
      setMsg(e.message)
    } finally {
      setSavingId(null)
    }
  }

  const deleteProgram = async (p: any) => {
    if (!confirm(`"${p.program_name}" programı kalıcı olarak silinsin mi? Bu işlem geri alınamaz.`)) return
    setSavingId(p.id)
    try {
      await admin.deleteProgram(p.id)
      setPrograms((ps) => ps.filter((x) => x.id !== p.id))
      setMsg(`Silindi: ${p.program_name}`)
    } catch (e: any) {
      setMsg(e.message)
    } finally {
      setSavingId(null)
    }
  }

  const refresh = async () => {
    setBusy(true)
    setMsg('KOSGEB sitesinden güncel veriler çekiliyor… Bu işlem 1-2 dakika sürebilir, lütfen bekleyin.')
    try {
      await admin.refreshPrograms()
      const initial = proposals.length
      let tries = 0
      const poll = async () => {
        tries++
        try {
          const list = await admin.proposals('pending')
          if (list.length !== initial) {
            setProposals(list)
            setMsg(`Tarama tamamlandı: onay bekleyen ${list.length} öneri listede.`)
            loadPrograms()
            setBusy(false)
            return
          }
        } catch {}
        if (tries >= 25) {
          setMsg('Tarama tamamlandı (veya yeni bir değişiklik bulunamadı). Listeyi kontrol edebilirsiniz.')
          setBusy(false)
          return
        }
        setTimeout(poll, 6000)
      }
      setTimeout(poll, 6000)
    } catch (e: any) {
      setMsg('Tarama başlatılamadı: ' + e.message)
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
                <strong>{p.proposed_data?.program_name || p.current_data?.program_name || p.program_code}</strong>
                <span style={{ marginLeft: 8, fontSize: 12, padding: '2px 8px', borderRadius: 4, color: '#fff',
                  background: p.change_type === 'create' ? '#1e8449' : p.change_type === 'deactivate' ? '#c0392b' : '#d68910' }}>
                  {p.change_type === 'create' ? 'YENİ PROGRAM' : p.change_type === 'deactivate' ? 'KALDIRMA' : 'GÜNCELLEME'}
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
            {p.diff_summary?.note && (
              <div style={{ marginTop: 12, fontSize: 13, color: '#c0392b', background: '#fdf0ef', padding: 10, borderRadius: 6 }}>
                {p.diff_summary.note}
              </div>
            )}
            {p.change_type === 'create' && p.proposed_data?.purpose && (
              <div style={{ marginTop: 12, fontSize: 13, color: '#4a4a44' }}>{p.proposed_data.purpose}</div>
            )}
            {p.source_url && (
              <div style={{ marginTop: 8, fontSize: 12, color: '#a8a79f' }}>
                Kaynak: <a href={p.source_url} target="_blank" rel="noreferrer" style={{ color: '#6b6a62' }}>detay sayfası</a> · Güven: {p.confidence}
              </div>
            )}
          </div>
        ))
      )}

      {/* ── Mevcut Programlar (doğrudan düzenleme) ── */}
      <h2 style={{ fontSize: 18, fontWeight: 700, margin: '32px 0 8px' }}>Mevcut Programlar</h2>
      <p style={{ color: '#6b6a62', fontSize: 14, marginBottom: 16 }}>
        Hero'daki "son başvuru tarihi" en yakın aktif programdan otomatik gelir. Yanlışsa ilgili programın
        tarihini buradan düzeltin veya programı pasife alın. Değişiklik birkaç dakikada siteye yansır.
      </p>
      {programs.map((p) => (
        <div key={p.id} style={{ border: '1px solid #e4e3dc', borderRadius: 8, padding: 14, marginBottom: 10, display: 'flex', gap: 12, alignItems: 'center', flexWrap: 'wrap' }}>
          <input
            value={p.program_name || ''}
            onChange={(e) => setProg(p.id, 'program_name', e.target.value)}
            style={{ flex: '1 1 260px', fontWeight: 600, fontSize: 14, padding: '6px 8px', border: '1px solid #d8d8d8', borderRadius: 6 }}
          />
          <label style={{ fontSize: 12, color: '#6b6a62' }}>Başlangıç
            <input type="date" value={p.application_period_start || ''} onChange={(e) => setProg(p.id, 'application_period_start', e.target.value)}
              style={{ display: 'block', padding: '6px 8px', border: '1px solid #d8d8d8', borderRadius: 6 }} />
          </label>
          <label style={{ fontSize: 12, color: '#6b6a62' }}>Son başvuru
            <input type="date" value={p.application_period_end || ''} onChange={(e) => setProg(p.id, 'application_period_end', e.target.value)}
              style={{ display: 'block', padding: '6px 8px', border: '1px solid #d8d8d8', borderRadius: 6 }} />
          </label>
          <label style={{ fontSize: 13, display: 'flex', alignItems: 'center', gap: 6 }}>
            <input type="checkbox" checked={!!p.is_active} onChange={(e) => setProg(p.id, 'is_active', e.target.checked)} /> Aktif
          </label>
          <button onClick={() => saveProgram(p)} disabled={savingId === p.id}
            style={{ background: '#003366', color: '#fff', border: 0, borderRadius: 6, padding: '8px 14px', cursor: 'pointer' }}>
            {savingId === p.id ? '…' : 'Kaydet'}
          </button>
          <button onClick={() => deleteProgram(p)} disabled={savingId === p.id}
            style={{ background: '#fff', color: '#c0392b', border: '1px solid #c0392b', borderRadius: 6, padding: '8px 14px', cursor: 'pointer' }}>
            Sil
          </button>
          {(p.purpose || (p.support_items && p.support_items.length > 0)) && (
            <details style={{ flexBasis: '100%', marginTop: 8, fontSize: 13, color: '#4a4a44' }}>
              <summary style={{ cursor: 'pointer', color: '#6b6a62' }}>Çekilen detaylar (amaç, destek unsurları)</summary>
              {p.purpose && <p style={{ marginTop: 8 }}>{p.purpose}</p>}
              {p.support_items && p.support_items.length > 0 && (
                <table style={{ width: '100%', fontSize: 12, borderCollapse: 'collapse', marginTop: 8 }}>
                  <thead>
                    <tr style={{ textAlign: 'left', color: '#6b6a62' }}>
                      <th style={{ padding: '4px 6px' }}>Destek Unsuru</th>
                      <th style={{ padding: '4px 6px' }}>Tutar</th>
                      <th style={{ padding: '4px 6px' }}>Oran</th>
                      <th style={{ padding: '4px 6px' }}>Süre</th>
                    </tr>
                  </thead>
                  <tbody>
                    {p.support_items.map((it: any, idx: number) => (
                      <tr key={idx} style={{ borderTop: '1px solid #eee' }}>
                        <td style={{ padding: '4px 6px' }}>{it.unsur}</td>
                        <td style={{ padding: '4px 6px' }}>{it.tutar}</td>
                        <td style={{ padding: '4px 6px' }}>{it.oran}</td>
                        <td style={{ padding: '4px 6px' }}>{it.sure}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </details>
          )}
        </div>
      ))}
    </div>
  )
}
