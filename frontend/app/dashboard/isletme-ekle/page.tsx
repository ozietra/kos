'use client'

import { useState, FormEvent } from 'react'
import DashboardLayout from '@/components/DashboardLayout'
import { useDashboardAuth } from '@/hooks/useDashboardAuth'
import { businesses, nace } from '@/lib/api'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import styles from './page.module.css'

export default function IsletmeEklePage() {
  const { user, loading } = useDashboardAuth()
  const router = useRouter()

  const [form, setForm] = useState({
    business_name: '',
    nace_code: '',
    nace_description: '',
    founding_date: '',
    employee_count: '',
    annual_revenue: '',
    city: '',
    is_woman_entrepreneur: false,
    is_young_entrepreneur: false,
    is_disabled: false,
    is_veteran: false,
    tax_number: '',
    sector_description: '',
    kosgeb_registered: false,
    has_recent_partnership: false,
  })

  const [naceSuggestQuery, setNaceSuggestQuery] = useState('')
  const [naceLoading, setNaceLoading] = useState(false)
  const [naceSuggestion, setNaceSuggestion] = useState<any>(null)

  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  function setField(key: string, value: any) {
    setForm(prev => ({ ...prev, [key]: value }))
  }

  async function handleNaceSuggest() {
    if (!naceSuggestQuery.trim()) return
    setNaceLoading(true)
    setNaceSuggestion(null)
    try {
      const suggestion = await nace.suggest(naceSuggestQuery)
      setNaceSuggestion(suggestion)
    } catch (e: any) {
      // Sessizce devam et
    } finally {
      setNaceLoading(false)
    }
  }

  function applyNace(code: string, desc: string) {
    setField('nace_code', code)
    setField('nace_description', desc)
    setNaceSuggestion(null)
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    setSaving(true)
    try {
      const payload = {
        ...form,
        employee_count: form.employee_count ? parseInt(form.employee_count) : null,
        annual_revenue: form.annual_revenue ? parseInt(form.annual_revenue) : null,
        founding_date: form.founding_date || null,
        tax_number: form.tax_number || null,
      }
      const biz = await businesses.create(payload)
      router.push(`/dashboard/isletme/${biz.id}`)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  if (loading) return null

  return (
    <DashboardLayout>
      <div className={styles.page}>
        <div className={styles.header}>
          <Link href="/dashboard" className="btn btn-secondary btn-sm">← Geri</Link>
          <h1 className={styles.title}>İşletme Ekle</h1>
        </div>

        {error && <div className="alert alert-danger" style={{ marginBottom: '20px' }}>{error}</div>}

        <form onSubmit={handleSubmit} className={styles.form}>
          {/* Temel bilgiler */}
          <div className="card" style={{ marginBottom: '20px' }}>
            <div className="card-title" style={{ marginBottom: '16px' }}>Temel Bilgiler</div>
            <div className={styles.grid2}>
              <div className="form-group">
                <label className="form-label">İşletme / Unvan <span style={{ color: 'var(--color-danger)' }}>*</span></label>
                <input className="input" required value={form.business_name}
                  onChange={e => setField('business_name', e.target.value)}
                  placeholder="ABC Tekstil San. Tic. Ltd. Şti." />
              </div>
              <div className="form-group">
                <label className="form-label">Şehir</label>
                <input className="input" value={form.city}
                  onChange={e => setField('city', e.target.value)} placeholder="İstanbul" />
              </div>
              <div className="form-group">
                <label className="form-label">Kuruluş Tarihi</label>
                <input className="input" type="date" value={form.founding_date}
                  onChange={e => setField('founding_date', e.target.value)} />
              </div>
              <div className="form-group">
                <label className="form-label">Çalışan Sayısı</label>
                <input className="input" type="number" min="1" value={form.employee_count}
                  onChange={e => setField('employee_count', e.target.value)} placeholder="5" />
              </div>
              <div className="form-group">
                <label className="form-label">Yıllık Ciro (₺)</label>
                <input className="input" type="number" value={form.annual_revenue}
                  onChange={e => setField('annual_revenue', e.target.value)} placeholder="2000000" />
              </div>
              <div className="form-group">
                <label className="form-label">Vergi No (şifreli saklanır)</label>
                <input className="input" value={form.tax_number}
                  onChange={e => setField('tax_number', e.target.value)} placeholder="1234567890" />
              </div>
            </div>
          </div>

          {/* NACE */}
          <div className="card" style={{ marginBottom: '20px' }}>
            <div className="card-title" style={{ marginBottom: '8px' }}>NACE Kodu</div>
            <p className="text-secondary fs-sm" style={{ marginBottom: '14px' }}>
              Sektörünüzü Türkçe açıklayın, sistem uygun NACE kodunu önerir.
            </p>
            <div className={styles.naceRow}>
              <input className="input" style={{ flex: 1 }}
                value={naceSuggestQuery}
                onChange={e => setNaceSuggestQuery(e.target.value)}
                placeholder="Örn: Tekstil konfeksiyon üretimi ve ihracatı yapıyorum"
                onKeyDown={e => e.key === 'Enter' && (e.preventDefault(), handleNaceSuggest())}
              />
              <button type="button" className="btn btn-secondary" onClick={handleNaceSuggest} disabled={naceLoading}>
                {naceLoading ? '...' : 'Öner'}
              </button>
            </div>

            {naceSuggestion && (
              <div className={styles.naceSuggestion}>
                <div className={styles.naceMain}>
                  <div>
                    <span className="fw-600">{naceSuggestion.nace_code}</span>
                    {' — '}{naceSuggestion.nace_description}
                  </div>
                  <div className="flex gap-8" style={{ marginTop: '4px' }}>
                    <span className={`badge ${naceSuggestion.is_kosgeb_eligible ? 'badge-success' : 'badge-danger'}`}>
                      {naceSuggestion.is_kosgeb_eligible ? 'KOSGEB Uygun' : 'KOSGEB Dışı'}
                    </span>
                    <span className="badge badge-muted">Güven: {naceSuggestion.confidence}</span>
                  </div>
                </div>
                <button type="button" className="btn btn-primary btn-sm"
                  onClick={() => applyNace(naceSuggestion.nace_code, naceSuggestion.nace_description)}>
                  Uygula
                </button>
              </div>
            )}

            <div className={styles.grid2} style={{ marginTop: '12px' }}>
              <div className="form-group">
                <label className="form-label">NACE Kodu</label>
                <input className="input" value={form.nace_code}
                  onChange={e => setField('nace_code', e.target.value)} placeholder="62.01" />
              </div>
              <div className="form-group">
                <label className="form-label">NACE Açıklaması</label>
                <input className="input" value={form.nace_description}
                  onChange={e => setField('nace_description', e.target.value)}
                  placeholder="Bilgisayar programlama faaliyetleri" />
              </div>
            </div>

            <div className="form-group" style={{ marginTop: '12px' }}>
              <label className="form-label">Sektör / Faaliyet Açıklaması</label>
              <textarea className="textarea" rows={3} value={form.sector_description}
                onChange={e => setField('sector_description', e.target.value)}
                placeholder="İşletmenizin ne yaptığını kısaca açıklayın..." />
            </div>
          </div>

          {/* Özel kategoriler */}
          <div className="card" style={{ marginBottom: '20px' }}>
            <div className="card-title" style={{ marginBottom: '12px' }}>Özel Girişimci Kategorisi</div>
            <p className="text-secondary fs-sm" style={{ marginBottom: '12px' }}>
              Aşağıdaki kategorilerden birine giriyorsanız işaretleyin. Hibe limitini 150.000 ₺ artırabilir.
            </p>
            <div className={styles.checkboxGroup}>
              {[
                { key: 'is_woman_entrepreneur', label: 'Kadın girişimci' },
                { key: 'is_young_entrepreneur', label: 'Genç girişimci (18-35 yaş)' },
                { key: 'is_disabled', label: 'Engelli girişimci' },
                { key: 'is_veteran', label: 'Şehit/Gazi yakını' },
              ].map(({ key, label }) => (
                <label key={key} className={styles.checkLabel}>
                  <input type="checkbox" checked={(form as any)[key]}
                    onChange={e => setField(key, e.target.checked)} />
                  {label}
                </label>
              ))}
            </div>
          </div>

          {/* KOSGEB durumu */}
          <div className="card" style={{ marginBottom: '28px' }}>
            <div className="card-title" style={{ marginBottom: '12px' }}>KOSGEB Durumu</div>
            <div className={styles.checkboxGroup}>
              <label className={styles.checkLabel}>
                <input type="checkbox" checked={form.kosgeb_registered}
                  onChange={e => setField('kosgeb_registered', e.target.checked)} />
                KOSGEB veri tabanında kayıtlıyım ve kaydım güncel/ aktif
              </label>
              <label className={styles.checkLabel}>
                <input type="checkbox" checked={form.has_recent_partnership}
                  onChange={e => setField('has_recent_partnership', e.target.checked)} />
                Son 3 yılda başka bir şirkette %25+ ortaklığım var (olabilir)
              </label>
            </div>
          </div>

          <button type="submit" className="btn btn-primary btn-lg" disabled={saving}>
            {saving ? 'Kaydediliyor...' : 'İşletmeyi Kaydet →'}
          </button>
        </form>
      </div>
    </DashboardLayout>
  )
}
