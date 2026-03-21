'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import DashboardLayout from '@/components/DashboardLayout'
import { useDashboardAuth } from '@/hooks/useDashboardAuth'
import { businesses, eligibility, applications } from '@/lib/api'
import Link from 'next/link'
import styles from './page.module.css'

export default function IsletmeDetayPage() {
  const { id } = useParams<{ id: string }>()
  const { user, loading } = useDashboardAuth()
  const router = useRouter()

  const [business, setBusiness] = useState<any>(null)
  const [eligResult, setEligResult] = useState<any>(null)
  const [checking, setChecking] = useState(false)
  const [starting, setStarting] = useState(false)
  const [selectedProgram, setSelectedProgram] = useState('')

  useEffect(() => {
    if (!loading && user) {
      businesses.get(id).then(setBusiness).catch(() => router.push('/dashboard'))
      eligibility.getLast(id).then(setEligResult).catch(() => {})
    }
  }, [loading, user, id])

  async function runEligibility() {
    setChecking(true)
    try {
      const result = await eligibility.check(id)
      setEligResult(result)
    } catch (e: any) {
      alert(e.message)
    } finally {
      setChecking(false)
    }
  }

  async function startApplication() {
    if (!selectedProgram) return
    setStarting(true)
    try {
      const app = await applications.create({
        business_id: id,
        program_type: selectedProgram,
        application_year: 2026,
      })
      router.push(`/dashboard/basvuru/${app.id}`)
    } catch (e: any) {
      alert(e.message)
    } finally {
      setStarting(false)
    }
  }

  if (loading || !business) return null

  // İş yaşını hesapla
  let ageText = ''
  if (business.founding_date) {
    const months = Math.floor(
      (Date.now() - new Date(business.founding_date).getTime()) / (1000 * 60 * 60 * 24 * 30)
    )
    ageText = months < 12 ? `${months} aylık` : `${Math.floor(months / 12)} yıl ${months % 12} aylık`
  }

  return (
    <DashboardLayout>
      <div className={styles.page}>
        <div className={styles.header}>
          <Link href="/dashboard" className="btn btn-secondary btn-sm">← Geri</Link>
          <h1 className={styles.title}>{business.business_name}</h1>
          <Link href={`/dashboard/isletme-ekle?edit=${id}`} className="btn btn-secondary btn-sm">
            Düzenle
          </Link>
        </div>

        {/* İşletme özeti */}
        <div className="card" style={{ marginBottom: '20px' }}>
          <div className={styles.metaGrid}>
            <div className={styles.metaItem}>
              <div className="label">NACE Kodu</div>
              <div className="fw-600">{business.nace_code || '—'}</div>
              <div className="fs-sm text-secondary">{business.nace_description || ''}</div>
            </div>
            <div className={styles.metaItem}>
              <div className="label">Şehir</div>
              <div className="fw-600">{business.city || '—'}</div>
            </div>
            <div className={styles.metaItem}>
              <div className="label">İşletme Yaşı</div>
              <div className="fw-600">{ageText || '—'}</div>
            </div>
            <div className={styles.metaItem}>
              <div className="label">Çalışan</div>
              <div className="fw-600">{business.employee_count ?? '—'}</div>
            </div>
            <div className={styles.metaItem}>
              <div className="label">KOSGEB Kaydı</div>
              <span className={`badge ${business.kosgeb_registered ? 'badge-success' : 'badge-warning'}`}>
                {business.kosgeb_registered ? 'Aktif ✓' : 'Kontrol edin'}
              </span>
            </div>
            <div className={styles.metaItem}>
              <div className="label">Özel Kategori</div>
              <div className="fw-600 fs-sm">
                {[
                  business.is_woman_entrepreneur && 'Kadın',
                  business.is_young_entrepreneur && 'Genç',
                  business.is_disabled && 'Engelli',
                  business.is_veteran && 'Şehit/Gazi',
                ].filter(Boolean).join(', ') || '—'}
              </div>
            </div>
          </div>
        </div>

        {/* Uygunluk */}
        <div className="card" style={{ marginBottom: '20px' }}>
          <div className={styles.eligHeader}>
            <div className="card-title">Uygunluk Analizi</div>
            <button className="btn btn-secondary btn-sm" onClick={runEligibility} disabled={checking}>
              {checking ? 'Analiz yapılıyor...' : eligResult ? 'Yenile' : 'Uygunluk Analizi Başlat'}
            </button>
          </div>

          {!eligResult && !checking && (
            <p className="text-secondary fs-sm" style={{ marginTop: '10px' }}>
              Hangi programlara başvurabileceğinizi görmek için analiz başlatın.
            </p>
          )}

          {eligResult && (
            <>
              {/* Uyarılar */}
              {eligResult.warnings?.map((w: any, i: number) => (
                <div key={i} className={`alert alert-${w.type === 'critical' ? 'danger' : w.type === 'warning' ? 'warning' : 'info'}`}
                  style={{ marginTop: '14px' }}>
                  {w.message}
                </div>
              ))}

              {/* Uygun programlar */}
              {eligResult.eligible?.length > 0 && (
                <div style={{ marginTop: '16px' }}>
                  <div className="label" style={{ marginBottom: '10px', color: 'var(--color-success)' }}>
                    ✓ Uygun Olduğunuz Programlar ({eligResult.eligible.length})
                  </div>
                  {eligResult.eligible.map((p: any, i: number) => (
                    <div key={i} className={styles.programCard}>
                      <div className={styles.programInfo}>
                        <div className="fw-600">{p.program_name}</div>
                        <div className="text-secondary fs-sm">
                          {p.key_requirements.join(' • ')}
                        </div>
                        {p.application_deadline && (
                          <div className="fs-xs text-muted">
                            Son başvuru: {new Date(p.application_deadline).toLocaleDateString('tr-TR')}
                          </div>
                        )}
                      </div>
                      <div style={{ textAlign: 'right', flexShrink: 0 }}>
                        <div className="amount" style={{ fontSize: '18px' }}>
                          {p.max_amount.toLocaleString('tr-TR')} ₺
                        </div>
                        <div className="fs-xs text-muted">{p.support_type}</div>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Uygun olmayan */}
              {eligResult.ineligible?.length > 0 && (
                <details style={{ marginTop: '16px' }}>
                  <summary className="text-secondary fs-sm" style={{ cursor: 'pointer', userSelect: 'none' }}>
                    ✗ Uygun Olmayan Programlar ({eligResult.ineligible.length}) — detaylar için tıklayın
                  </summary>
                  <div style={{ marginTop: '10px' }}>
                    {eligResult.ineligible.map((p: any, i: number) => (
                      <div key={i} className={styles.ineligibleCard}>
                        <div className="fw-600">{p.program_name}</div>
                        <div className="fs-sm text-secondary">{p.reason}</div>
                      </div>
                    ))}
                  </div>
                </details>
              )}
            </>
          )}
        </div>

        {/* Başvuru başlat */}
        {eligResult?.eligible?.length > 0 && (
          <div className="card">
            <div className="card-title" style={{ marginBottom: '14px' }}>Başvuru Başlat</div>
            <div className="form-group" style={{ marginBottom: '16px' }}>
              <label className="form-label">Program Seçin</label>
              <select className="select" value={selectedProgram}
                onChange={e => setSelectedProgram(e.target.value)}>
                <option value="">— Program Seçin —</option>
                {eligResult.eligible.map((p: any) => (
                  <option key={p.program_id} value={p.program_name}>
                    {p.program_name} ({p.max_amount.toLocaleString('tr-TR')} ₺)
                  </option>
                ))}
              </select>
            </div>
            <button
              className="btn btn-primary btn-lg"
              onClick={startApplication}
              disabled={!selectedProgram || starting}
            >
              {starting ? 'Başlatılıyor...' : 'Başvuruyu Hazırla →'}
            </button>
            <p className="fs-xs text-muted" style={{ marginTop: '10px' }}>
              Ödeme, başvuru metni tamamlandıktan sonra alınır.
            </p>
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}
