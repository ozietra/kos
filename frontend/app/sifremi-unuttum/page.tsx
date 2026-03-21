'use client'

import { useState, FormEvent } from 'react'
import Link from 'next/link'
import { auth } from '@/lib/api'
import styles from './../auth.module.css'

export default function SifremiUnuttumPage() {
  const [email, setEmail] = useState('')
  const [sent, setSent] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await auth.forgotPassword(email)
      setSent(true)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles.page}>
      <div className={styles.card}>
        <Link href="/" className={styles.logo}>
          kosgeb<span>hibe</span>.com
        </Link>
        <h1 className={styles.title}>Şifremi Unuttum</h1>

        {sent ? (
          <div className="alert alert-success">
            E-posta adresinize şifre sıfırlama bağlantısı gönderildi.
            Spam klasörünüzü de kontrol edin.
          </div>
        ) : (
          <>
            {error && <div className="alert alert-danger" style={{ marginBottom: '16px' }}>{error}</div>}
            <form onSubmit={handleSubmit} className={styles.form}>
              <div className="form-group">
                <label className="form-label" htmlFor="email">Kayıtlı E-posta Adresiniz</label>
                <input
                  id="email"
                  type="email"
                  className="input"
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  required
                  placeholder="ornek@firma.com"
                />
              </div>
              <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={loading}>
                {loading ? 'Gönderiliyor...' : 'Sıfırlama Bağlantısı Gönder'}
              </button>
            </form>
          </>
        )}

        <p className={styles.switchLink}>
          <Link href="/giris">← Giriş Yap</Link>
        </p>
      </div>
    </div>
  )
}
