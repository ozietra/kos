'use client'

import { useState, FormEvent } from 'react'
import { useParams, useRouter } from 'next/navigation'
import DashboardLayout from '@/components/DashboardLayout'
import { useDashboardAuth } from '@/hooks/useDashboardAuth'
import { applications } from '@/lib/api'
import Link from 'next/link'
import styles from './page.module.css'

const STEPS = [
  { num: 1, label: 'Proje Fikri' },
  { num: 2, label: 'Pazar' },
  { num: 3, label: 'Finansal' },
  { num: 4, label: 'Zaman' },
]

export default function BasvuruFormPage() {
  const { id: applicationId } = useParams<{ id: string }>()
  const { user, loading } = useDashboardAuth()
  const router = useRouter()
  const [step, setStep] = useState(1)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  const [form, setForm] = useState({
    // Adım 1
    project_title: '',
    project_idea: '',
    problem_solved: '',
    // Adım 2
    target_market: '',
    competitors: '',
    competitive_advantage: '',
    market_size: '',
    // Adım 3
    requested_amount: '',
    budget_items: '',
    revenue_target_year1: '',
    employment_target: '',
    // Adım 4
    project_duration_months: '12',
    milestones: '',
  })

  function setField(key: string, value: string) {
    setForm(prev => ({ ...prev, [key]: value }))
  }

  async function saveStep() {
    setSaving(true)
    setError('')
    try {
      await applications.saveInputs(applicationId, {
        ...form,
        requested_amount: form.requested_amount ? parseInt(form.requested_amount) : undefined,
        revenue_target_year1: form.revenue_target_year1 ? parseInt(form.revenue_target_year1) : undefined,
        employment_target: form.employment_target ? parseInt(form.employment_target) : undefined,
        project_duration_months: form.project_duration_months ? parseInt(form.project_duration_months) : undefined,
      })
    } catch (e: any) {
      setError(e.message)
      return false
    } finally {
      setSaving(false)
    }
    return true
  }

  async function handleNext(e: FormEvent) {
    e.preventDefault()
    const ok = await saveStep()
    if (!ok) return
    if (step < 4) {
      setStep(step + 1)
    } else {
      // Son adım: üretim sayfasına yönlendir
      router.push(`/dashboard/basvuru/${applicationId}/uret`)
    }
  }

  if (loading) return null

  return (
    <DashboardLayout>
      <div className={styles.page}>
        {/* Adım göstergesi */}
        <div className={styles.stepper}>
          {STEPS.map((s, i) => (
            <div key={s.num} className={styles.stepperItem}>
              <div className={`${styles.stepperDot} ${step > s.num ? styles.done : step === s.num ? styles.active : ''}`}>
                {step > s.num ? '✓' : s.num}
              </div>
              <span className={`${styles.stepperLabel} ${step === s.num ? styles.activeLabel : ''}`}>
                {s.label}
              </span>
              {i < STEPS.length - 1 && <div className={`${styles.stepperLine} ${step > s.num ? styles.lineDone : ''}`} />}
            </div>
          ))}
        </div>

        {error && <div className="alert alert-danger" style={{ marginBottom: '16px' }}>{error}</div>}

        <form onSubmit={handleNext} className={styles.form}>
          {/* ADIM 1 */}
          {step === 1 && (
            <div className="card">
              <div className="card-title" style={{ marginBottom: '16px' }}>Proje Fikriniz</div>
              <div className={styles.fields}>
                <div className="form-group">
                  <label className="form-label">Proje Başlığı <span style={{ color: 'var(--color-danger)' }}>*</span></label>
                  <input className="input" required maxLength={120} value={form.project_title}
                    onChange={e => setField('project_title', e.target.value)}
                    placeholder="Örnek: Tekstil atölyemiz için tam otomatik kesim hattı kurulumu" />
                  <div className="form-hint">Kısa, net ve proje hedefini özetler nitelikte olsun.</div>
                </div>
                <div className="form-group">
                  <label className="form-label">Proje Fikri ve Amacı <span style={{ color: 'var(--color-danger)' }}>*</span></label>
                  <textarea className="textarea" required rows={4} value={form.project_idea}
                    onChange={e => setField('project_idea', e.target.value)}
                    placeholder="Bu projeyle ne yapmak istiyorsunuz? Neyi değiştirmek/geliştirmek istiyorsunuz?" />
                </div>
                <div className="form-group">
                  <label className="form-label">Çözülen Problem <span style={{ color: 'var(--color-danger)' }}>*</span></label>
                  <textarea className="textarea" required rows={3} value={form.problem_solved}
                    onChange={e => setField('problem_solved', e.target.value)}
                    placeholder="Şu an hangi sorunu yaşıyorsunuz? Bu proje o sorunu nasıl çözüyor?" />
                </div>
              </div>
            </div>
          )}

          {/* ADIM 2 */}
          {step === 2 && (
            <div className="card">
              <div className="card-title" style={{ marginBottom: '16px' }}>Pazar Analizi</div>
              <div className={styles.fields}>
                <div className="form-group">
                  <label className="form-label">Hedef Kitle <span style={{ color: 'var(--color-danger)' }}>*</span></label>
                  <textarea className="textarea" required rows={3} value={form.target_market}
                    onChange={e => setField('target_market', e.target.value)}
                    placeholder="Ürününüzü/hizmetinizi kimler kullanacak? Kaç potansiyel müşteri var?" />
                </div>
                <div className="form-group">
                  <label className="form-label">Rakipler</label>
                  <textarea className="textarea" rows={2} value={form.competitors}
                    onChange={e => setField('competitors', e.target.value)}
                    placeholder="Piyasada sizinle benzer iş yapan firmalar var mı? Kimleri biliyorsunuz?" />
                </div>
                <div className="form-group">
                  <label className="form-label">Rekabetçi Avantajınız <span style={{ color: 'var(--color-danger)' }}>*</span></label>
                  <textarea className="textarea" required rows={3} value={form.competitive_advantage}
                    onChange={e => setField('competitive_advantage', e.target.value)}
                    placeholder="Rakiplerinizden sizi ayıran nedir? Neden müşteriler sizi tercih etmeli?" />
                </div>
                <div className="form-group">
                  <label className="form-label">Pazar Büyüklüğü</label>
                  <input className="input" value={form.market_size}
                    onChange={e => setField('market_size', e.target.value)}
                    placeholder="Türkiye'de bu sektörün tahmini büyüklüğü (₺ veya ürün adedi)" />
                </div>
              </div>
            </div>
          )}

          {/* ADIM 3 */}
          {step === 3 && (
            <div className="card">
              <div className="card-title" style={{ marginBottom: '16px' }}>Finansal Bilgiler</div>
              <div className={styles.fields}>
                <div className="form-group">
                  <label className="form-label">
                    Talep Ettiğiniz Destek Miktarı (₺) <span style={{ color: 'var(--color-danger)' }}>*</span>
                  </label>
                  <input className="input" type="number" required value={form.requested_amount}
                    onChange={e => setField('requested_amount', e.target.value)}
                    placeholder="500000" />
                  <div className="form-hint">İş Geliştirme Desteği limiti 1.500.000 ₺'dir.</div>
                </div>
                <div className="form-group">
                  <label className="form-label">
                    Bütçe Kalemleri <span style={{ color: 'var(--color-danger)' }}>*</span>
                  </label>
                  <textarea className="textarea" required rows={4} value={form.budget_items}
                    onChange={e => setField('budget_items', e.target.value)}
                    placeholder={`Makine/ekipman: 300.000 ₺\nYazılım: 100.000 ₺\nEğitim: 50.000 ₺\nToplam: 450.000 ₺`} />
                </div>
                <div className="form-group">
                  <label className="form-label">
                    1. Yıl Gelir Hedefi (₺) <span style={{ color: 'var(--color-danger)' }}>*</span>
                  </label>
                  <input className="input" type="number" required value={form.revenue_target_year1}
                    onChange={e => setField('revenue_target_year1', e.target.value)}
                    placeholder="2000000" />
                </div>
                <div className="form-group">
                  <label className="form-label">Yeni İstihdam Hedefi (kişi) <span style={{ color: 'var(--color-danger)' }}>*</span></label>
                  <input className="input" type="number" required value={form.employment_target}
                    onChange={e => setField('employment_target', e.target.value)} placeholder="3" />
                  <div className="form-hint">Proje tamamlandığında kaç kişi daha istihdam edeceksiniz?</div>
                </div>
              </div>
            </div>
          )}

          {/* ADIM 4 */}
          {step === 4 && (
            <div className="card">
              <div className="card-title" style={{ marginBottom: '16px' }}>Proje Takvimi</div>
              <div className={styles.fields}>
                <div className="form-group">
                  <label className="form-label">
                    Proje Süresi (ay) <span style={{ color: 'var(--color-danger)' }}>*</span>
                  </label>
                  <select className="select" required value={form.project_duration_months}
                    onChange={e => setField('project_duration_months', e.target.value)}>
                    {[6, 9, 12, 18, 24].map(m => (
                      <option key={m} value={m}>{m} ay</option>
                    ))}
                  </select>
                </div>
                <div className="form-group">
                  <label className="form-label">
                    Kilometre Taşları <span style={{ color: 'var(--color-danger)' }}>*</span>
                  </label>
                  <textarea className="textarea" required rows={5} value={form.milestones}
                    onChange={e => setField('milestones', e.target.value)}
                    placeholder={`Ay 1-2: Tedarikçi seçimi ve sipariş\nAy 3-5: Kurulum ve devreye alma\nAy 6: Deneme üretimi\nAy 7-12: Tam kapasite üretim ve satış`} />
                </div>
                <div className="alert alert-info">
                  <strong>Son Adım.</strong> "Başvuruyu Hazırla" butonuna bastıktan sonra
                  sistem 3–5 dakikada başvuru metinlerinizi hazırlayacak.
                  Sonuçları kontrol edip PDF indirebileceksiniz.
                </div>
              </div>
            </div>
          )}

          <div className={styles.navBtns}>
            {step > 1 && (
              <button type="button" className="btn btn-secondary" onClick={() => setStep(step - 1)}>
                ← Geri
              </button>
            )}
            {step < 4 && (
              <button type="submit" className="btn btn-primary" disabled={saving}>
                {saving ? 'Kaydediliyor...' : 'İleri →'}
              </button>
            )}
            {step === 4 && (
              <button type="submit" className="btn btn-primary btn-lg" disabled={saving}>
                {saving ? 'Kaydediliyor...' : '🚀 Başvuruyu Hazırla'}
              </button>
            )}
          </div>
        </form>
      </div>
    </DashboardLayout>
  )
}
