'use client'

import { Suspense } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import DashboardLayout from '@/components/DashboardLayout'
import { useDashboardAuth } from '@/hooks/useDashboardAuth'
import { payments } from '@/lib/api'
import styles from './page.module.css'

function OdemeInner() {
  const { user, loading } = useDashboardAuth()
  const params = useSearchParams()
  const router = useRouter()
  const applicationId = params.get('basvuru')
  const plan = (params.get('plan') || 'starter') as 'starter' | 'pro'

  const [checkoutHtml, setCheckoutHtml] = useState<string | null>(null)
  const [checkoutUrl, setCheckoutUrl] = useState<string | null>(null)
  const [processing, setProcessing] = useState(false)
  const [error, setError] = useState('')

  const price = '499'
  const planLabel = 'Starter'

  async function loadCheckout() {
    if (!applicationId) return
    setProcessing(true)
    setError('')
    try {
      const data = await payments.checkout({ application_id: applicationId, plan })
      if (data.paymentPageUrl) {
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
    if (!loading && user && applicationId) {
      loadCheckout()
    }
  }, [loading, user, applicationId])

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
            <span>kosgebhibe.com {planLabel} Planı</span>
            <span className="fw-600">{parseInt(price).toLocaleString('tr-TR')} ₺</span>
          </div>
          <div className={styles.orderRow} style={{ fontSize: '12px', color: 'var(--color-text-muted)' }}>
            <span>KDV dahildir</span>
          </div>
          <div className={styles.divider} />
          <div className={styles.orderRow} style={{ fontWeight: '700' }}>
            <span>Toplam</span>
            <span className="amount">{parseInt(price).toLocaleString('tr-TR')} ₺</span>
          </div>
        </div>

        {error && (
          <div className="alert alert-danger" style={{ marginBottom: '16px', maxWidth: '480px' }}>
            {error}
          </div>
        )}

        {checkoutUrl && (
          <div style={{ maxWidth: '480px' }}>
            <p className="text-secondary fs-sm" style={{ marginBottom: '14px' }}>
              Güvenli ödeme sayfasına yönlendiriliyorsunuz...
            </p>
            <a href={checkoutUrl} className="btn btn-primary btn-lg">
              İyzico ile Güvenli Öde
            </a>
          </div>
        )}

        {checkoutHtml && (
          <div id="iyzico-checkout" style={{ maxWidth: '480px' }} />
        )}

        {processing && (
          <div className={styles.loading}>
            <div className={styles.spinner} />
            <p className="text-secondary fs-sm">Ödeme sayfası hazırlanıyor...</p>
          </div>
        )}

        <div className="legal-note" style={{ marginTop: '24px', maxWidth: '480px' }}>
          Ödeme iyzico güvenli altyapısı ile işlenir. Kart bilgileriniz kosgebhibe.com sunucularında saklanmaz.
          Ödeme yerine getirildikten sonra başvurunuza tam erişim sağlanır.
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
