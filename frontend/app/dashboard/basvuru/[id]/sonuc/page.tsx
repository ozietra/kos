'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import DashboardLayout from '@/components/DashboardLayout'
import { useDashboardAuth } from '@/hooks/useDashboardAuth'
import { applications } from '@/lib/api'
import Link from 'next/link'
import Icon from '@/components/Icon'
import styles from './page.module.css'

export default function SonucPage() {
  const { id } = useParams<{ id: string }>()
  const { user, loading } = useDashboardAuth()

  const [app, setApp] = useState<any>(null)
  const [docs, setDocs] = useState<any[]>([])
  const [downloading, setDownloading] = useState(false)

  useEffect(() => {
    if (!loading && user) {
      applications.get(id).then(setApp).catch(() => {})
      applications.getDocuments(id).then(setDocs).catch(() => {})
    }
  }, [loading, user, id])

  async function downloadPdf() {
    setDownloading(true)
    try {
      const url = applications.getPdfUrl(id)
      const token = localStorage.getItem('token')
      const res = await fetch(url, {
        headers: { Authorization: `Bearer ${token}` },
      })
      if (!res.ok) throw new Error('PDF indirme hatası.')
      const blob = await res.blob()
      const a = document.createElement('a')
      a.href = URL.createObjectURL(blob)
      a.download = `kosgeb-basvuru-${id}.pdf`
      a.click()
    } catch (e: any) {
      alert(e.message)
    } finally {
      setDownloading(false)
    }
  }

  if (loading || !app) return null

  return (
    <DashboardLayout>
      <div className={styles.page}>
        <div className={styles.pageHeader}>
          <div>
            <div className="badge badge-success" style={{ marginBottom: '10px' }}>✓ Başvuru Dosyası Tamamlandı</div>
            <h1 className={styles.title}>Başvurunuz Hazır</h1>
            <p className="text-secondary">
              {app.program_type} başvurusu için dosyanız oluşturuldu.
              PDF'i indirin, belgeleri toplayın ve e-Devlet'ten gönderin.
            </p>
          </div>
          <button
            className="btn btn-primary btn-lg"
            onClick={downloadPdf}
            disabled={downloading}
          >
            {downloading ? 'İndiriliyor...' : <><Icon name="document" size={18} /> PDF İndir</>}
          </button>
        </div>

        {/* Oluşturulan bölümler */}
        <div className={styles.sectionsGrid}>
          {[
            { key: 'project_summary', label: 'Proje Özeti' },
            { key: 'business_plan', label: 'İş Planı' },
            { key: 'financial_projection', label: 'Finansal Projeksiyon' },
            { key: 'timeline', label: 'Proje Takvimi' },
          ].map(({ key, label }) => (
            <div key={key} className={styles.sectionCard}>
              <div className="card-title">{label}</div>
              {app[key] ? (
                <div className={styles.preview}>
                  {app[key].slice(0, 300)}{app[key].length > 300 ? '...' : ''}
                </div>
              ) : (
                <p className="text-muted fs-sm">Oluşturulmadı.</p>
              )}
            </div>
          ))}
        </div>

        {/* Belge listesi */}
        {docs.length > 0 && (
          <div className="card" style={{ marginTop: '28px' }}>
            <div className="card-title" style={{ marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Icon name="clipboard" size={18} /> Belge Kontrol Listesi
            </div>
            <p className="text-secondary fs-sm" style={{ marginBottom: '16px' }}>
              Aşağıdaki belgeler başvurunuz için gereklidir. Topladıkça işaretleyin.
            </p>
            <div className={styles.docList}>
              {docs.map((doc, i) => (
                <label key={i} className={styles.docItem}>
                  <input type="checkbox" className={styles.docCheck} />
                  <div className={styles.docInfo}>
                    <div className="fw-600 fs-sm">{doc.name}</div>
                    <div className="fs-xs text-secondary">Nereden alınır: {doc.where_to_get}</div>
                    {doc.description && (
                      <div className="fs-xs text-muted">{doc.description}</div>
                    )}
                    {doc.note && (
                      <div className="alert alert-warning fs-xs" style={{ marginTop: '4px', padding: '6px 10px' }}>
                        {doc.note}
                      </div>
                    )}
                  </div>
                </label>
              ))}
            </div>
          </div>
        )}

        {/* Sonraki adımlar */}
        <div className="card" style={{ marginTop: '24px', background: 'var(--color-info-bg)', borderColor: 'var(--color-info)' }}>
          <div className="card-title" style={{ marginBottom: '10px' }}>Sonraki Adımlar</div>
          <ol className={styles.nextSteps}>
            <li>PDF'i indirin ve gözden geçirin.</li>
            <li>Belge listesindeki tüm evrakları toplayın.</li>
            <li>KOSGEB kaydınızın aktif olduğunu doğrulayın (<a href="https://kosgeb.gov.tr" target="_blank" rel="noopener noreferrer">kosgeb.gov.tr</a>).</li>
            <li>Vergi ve SGK borç sorgusunu yapın.</li>
            <li>Başvurunuzu KOSGEB e-Hizmetler üzerinden (<a href="https://kosgeb.gov.tr" target="_blank" rel="noopener noreferrer">kosgeb.gov.tr</a>, e-Devlet şifresiyle giriş) gönderin.</li>
          </ol>
        </div>

        <div className="legal-note" style={{ marginTop: '24px' }}>
          Bu belge bilgilendirme amaçlıdır. Güncel program şartları için{' '}
          <a href="https://kosgeb.gov.tr" target="_blank" rel="noopener noreferrer">kosgeb.gov.tr</a>{' '}
          ziyaret edin. Onay garantisi verilmez.
        </div>
      </div>
    </DashboardLayout>
  )
}
