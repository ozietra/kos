'use client'

import { Suspense } from 'react'
import { useSearchParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import DashboardLayout from '@/components/DashboardLayout'
import { useDashboardAuth } from '@/hooks/useDashboardAuth'
import { payments, content } from '@/lib/api'
import styles from './page.module.css'

function fmtTL(n: number) {
  const s = Number.isInteger(n) ? n.toLocaleString('tr-TR') : n.toLocaleString('tr-TR', { minimumFractionDigits: 2 })
  return `${s} ₺`
}

function OdemeInner() {
  const { user, loading } = useDashboardAuth()
  const params = useSearchParams()
  const applicationId = params.get('basvuru')
  const plan = params.get('plan') || 'starter'

  const [checkoutHtml, setCheckoutHtml] = useState<string | null>(null)
  const [checkoutUrl, setCheckoutUrl] = useState<string | null>(null)
  const [iframeSrc, setIframeSrc] = useState<string | null>(null)
  const [processing, setProcessing] = useState(false)
  const [error, setError] = useState('')
  const [provider, setProvider] = useState<'iyzico' | 'paytr'>('iyzico')
  const [planInfo, setPlanInfo] = useState<any>(null)

  const planLabel = planInfo?.name || 'Plan'
  const effective = planInfo?.effective_price ?? null

  useEffect(() => {
    content.pricing().then((r) => {
      const p = (r.plans || []).find((x: any) => x.code === plan) || (r.plans || [])[0]
      setPlanInfo(p)
    }).catch(() => {})
  }, [plan])

  async function loadCheckout() {
    if (!applicationId) return
    setProcessing(true)
    setError('')
    setCheckoutHtml(null); setCheckoutUrl(null); setIframeSrc(null)
    try {
      const data: any = await payments.checkout({ application_id: applicationId, plan, provider })
      if (data.provider === 'paytr' && data.iframe_url) {
        setIframeSrc(data.iframe_url)
      } else if (data.paymentPageUrl) {
        setCheckoutUrl(data.paymentPageUrl)
      } else if (data.checkoutFormContent) {
        setCheckoutHtml(data.checkoutFormContent)
      }
    } catch (e: any) {
      setError(e.message)
    } finally {
      setProcessing(false)
    }
  }

  useEffect(() => {
    if (checkoutHtml) {
      const div = document.getElementById('iyzico-checkout')
      if (div) {
        div.innerHTML = checkoutHtml
        Array.from(div.querySelectorAll('script')).forEach(oldScript => {
          const newScript = document.createElement('script')
          Array.from(oldScript.attributes).forEach(a => newScript.setAttribute(a.name, a.value))
          newScript.innerHTML = oldScript.innerHTML
          oldScript.parentNode?.replaceChild(newScript, oldScript)
        })
      }
    }
  }, [checkoutHtml])

  if (loading) return null

  if (!applicationId) {
    return (
      <DashboardLayout>
        <div className={styles.page}>
          <div className="alert alert-danger">Başvuru ID eksik. Lütfen başvurunuzu tekrar açın.</div>
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout>
      <div className={styles.page}>
        <h1 className={styles.title}>Ödeme</h1>

        <div className="card" style={{ marginBottom: '24px', maxWidth: '480px' }}>
          <div className="card-title" style={{ marginBottom: '14px' }}>Sipariş Özeti</div>
          <div className={styles.orderRow}>
            <span>{planLabel} Planı</span>
            <span className="fw-600">{effective != null ? fmtTL(effective) : '—'}</span>
          </div>
          {planInfo?.is_campaign && (
            <div className={styles.orderRow} style={{ fontSize: '12px', color: 'var(--color-success)' }}>
              <span>{planInfo.campaign_label || 'Kampanya indirimi'} uygulandı</span>
              <span style={{ textDecoration: 'line-through', opacity: 0.6 }}>{fmtTL(planInfo.price)}</span>
            </div>
          )}
          <div className={styles.orderRow} style={{ fontSize: '12px', color: 'var(--color-text-muted)' }}>
            <span>KDV dahildir</span>
          </div>
          <div className={styles.divider} />
          <div className={styles.orderRow} style={{ fontWeight: '700' }}>
            <span>Toplam</span>
            <span className="amount">{effective != null ? fmtTL(effective) : '—'}</span>
          </div>
        </div>

        {!iframeSrc && !checkoutHtml && !checkoutUrl && (
          <div className="card" style={{ marginBottom: '24px', maxWidth: '480px' }}>
            <div className="card-title" style={{ marginBottom: '12px' }}>Ödeme Yöntemi</div>
            <div style={{ display: 'flex', gap: 10, marginBottom: 16 }}>
              {(['iyzico', 'paytr'] as const).map((pv) => (
                <button
                  key={pv}
                  onClick={() => setProvider(pv)}
                  style={{
                    flex: 1, padding: '10px', borderRadius: 8, cursor: 'pointer', fontWeight: 600,
                    border: provider === pv ? '2px solid var(--color-accent)' : '1px solid #d8d8d8',
                    background: provider === pv ? 'rgba(192,57,43,0.06)' : '#fff',
                  }}
                >
                  {pv === 'iyzico' ? 'iyzico' : 'PayTR'}
                </button>
              ))}
            </div>
            <button onClick={loadCheckout} disabled={processing} className="btn btn-primary btn-lg" style={{ width: '100%' }}>
              {processing ? 'Hazırlanıyor…' : 'Güvenli Öde'}
            </button>
          </div>
        )}

        {error && (
          <div className="alert alert-danger" style={{ marginBottom: '16px', maxWidth: '480px' }}>
            {error}
          </div>
        )}

        {iframeSrc && (
          <iframe src={iframeSrc} style={{ width: '100%', maxWidth: 480, height: 700, border: 0 }} title="PayTR Ödeme" />
        )}

        {checkoutUrl && (
          <div style={{ maxWidth: '480px' }}>
            <p className="text-secondary fs-sm" style={{ marginBottom: '14px' }}>
              Güvenli ödeme sayfasına yönlendiriliyorsunuz...
            </p>
            <a href={checkoutUrl} className="btn btn-primary btn-lg">
              iyzico ile Güvenli Öde
            </a>
          </div>
        )}

        {checkoutHtml && (
          <div id="iyzico-checkout" style={{ maxWidth: '480px' }} />
        )}

        <div className="legal-note" style={{ marginTop: '24px', maxWidth: '480px' }}>
          Ödeme, seçtiğiniz güvenli ödeme altyapısı ile işlenir. Kart bilgileriniz sunucularımızda saklanmaz.
          Ödeme tamamlandıktan sonra başvurunuza tam erişim sağlanır.
        </div>
      </div>
    </DashboardLayout>
  )
}

export default function OdemePage() {
  return (
    <Suspense fallback={null}>
      <OdemeInner />
    </Suspense>
  )
}
