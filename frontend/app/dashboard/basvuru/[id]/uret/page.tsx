'use client'

import { useEffect, useRef, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import DashboardLayout from '@/components/DashboardLayout'
import { useDashboardAuth } from '@/hooks/useDashboardAuth'
import { applications } from '@/lib/api'
import Icon from '@/components/Icon'
import styles from './page.module.css'

const STEPS_LABELS: Record<string, string> = {
  'input_validation':    '1/7 Bilgiler doğrulanıyor...',
  'project_summary':     '2/7 Proje özeti hazırlanıyor...',
  'business_plan':       '3/7 İş planı yazılıyor...',
  'financial_projection':'4/7 Finansal projeksiyon oluşturuluyor...',
  'timeline':            '5/7 Proje takvimi düzenleniyor...',
  'documents':           '6/7 Belge listesi hazırlanıyor...',
  'finalizing':          '7/7 Başvuru dosyası tamamlanıyor...',
}

export default function UretimPage() {
  const { id } = useParams<{ id: string }>()
  const { user, loading } = useDashboardAuth()
  const router = useRouter()

  const [progress, setProgress] = useState(0)
  const [statusLabel, setStatusLabel] = useState('Hazırlanıyor...')
  const [started, setStarted] = useState(false)
  const [done, setDone] = useState(false)
  const [errorMsg, setErrorMsg] = useState('')
  const esRef = useRef<EventSource | null>(null)

  useEffect(() => {
    return () => {
      esRef.current?.close()
    }
  }, [])

  async function startGeneration() {
    setStarted(true)
    setProgress(0)
    setErrorMsg('')

    // 1. Üretimi başlat
    try {
      await applications.startGeneration(id)
    } catch (e: any) {
      setErrorMsg(e.message)
      setStarted(false)
      return
    }

    // 2. SSE dinle
    const url = applications.getProgressUrl(id)
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
    const es = new EventSource(`${url}?token=${token}`)
    esRef.current = es

    es.addEventListener('message', (e) => {
      const data = JSON.parse(e.data)
      
      if (data.error) {
        es.close()
        setErrorMsg(data.text || 'Üretim sırasında bir hata oluştu.')
        setStarted(false)
        return
      }

      setProgress(data.progress ?? 0)
      setStatusLabel(data.text || 'Devam ediyor...')

      if (data.progress >= 100 || data.done) {
        es.close()
        setDone(true)
        setTimeout(() => {
          router.push(`/dashboard/basvuru/${id}/sonuc`)
        }, 1200)
      }
    })

    es.addEventListener('error', () => {
      if (es.readyState === EventSource.CLOSED) {
        return // Normal kapanma
      }
      es.close()
      setErrorMsg('Bağlantı kesildi. Lütfen sayfayı yenileyip tekrar deneyin.')
      setStarted(false)
    })
  }

  if (loading) return null

  return (
    <DashboardLayout>
      <div className={styles.page}>
        <div className={styles.center}>
          <div className={styles.iconBig}>
            <Icon name={done ? 'checkCircle' : started ? 'gear' : 'document'} size={48} strokeWidth={1.5} />
          </div>
          <h1 className={styles.title}>
            {done ? 'Başvuru Dosyası Hazır!' :
             started ? 'Hazırlanıyor...' :
             'Başvuru Hazırlamaya Başla'}
          </h1>
          <p className="text-secondary" style={{ maxWidth: '420px', textAlign: 'center' }}>
            {done ? 'Yönlendiriliyorsunuz...' :
             started ? statusLabel :
             'Girdiğiniz bilgiler kullanılarak başvuru metinleriniz hazırlanacak. Bu işlem 3–5 dakika sürer.'}
          </p>

          {errorMsg && (
            <div className="alert alert-danger" style={{ marginTop: '20px', maxWidth: '420px' }}>
              {errorMsg}
            </div>
          )}

          {started && !done && (
            <div className={styles.progressSection}>
              <div className="progress-bar" style={{ width: '100%', maxWidth: '420px' }}>
                <div className="progress-fill" style={{ width: `${progress}%` }} />
              </div>
              <div className={styles.progressPct}>{progress}%</div>
            </div>
          )}

          {!started && !done && (
            <button className="btn btn-primary btn-lg" style={{ marginTop: '28px' }} onClick={startGeneration}>
              <Icon name="spark" size={18} /> Başvuruyu Hazırla
            </button>
          )}

          {started && !done && (
            <div className={styles.tipBox}>
              <div className="fw-600 fs-sm">Bu sürede yapabilecekleriniz:</div>
              <ul className="fs-sm text-secondary" style={{ marginTop: '8px', paddingLeft: '16px' }}>
                <li>Eksik belgelerinizi listelemek (ardından göreceksiniz)</li>
                <li>KOSGEB kaydınızın güncel olup olmadığını kontrol etmek</li>
                <li>Vergi/SGK borç sorgulaması yapmak (çevrimiçi)</li>
              </ul>
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  )
}
