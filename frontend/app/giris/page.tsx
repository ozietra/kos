'use client'

import { useState, FormEvent } from 'react'
import Link from 'next/link'
import { auth, tokenHelpers } from '@/lib/api'
import styles from './../auth.module.css'

export default function GirisPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const res = await auth.login(email, password)
      tokenHelpers.save(res.access_token)
      window.location.href = '/dashboard'
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
        <h1 className={styles.title}>Giriş Yap</h1>

        {error && <div className="alert alert-danger" style={{ marginBottom: '16px' }}>{error}</div>}

        <form onSubmit={handleSubmit} className={styles.form}>
          <div className="form-group">
            <label className="form-label" htmlFor="email">E-posta</label>
            <input
              id="email"
              type="email"
              className="input"
              value={email}
              onChange={e => setEmail(e.target.value)}
              required
              autoComplete="email"
              placeholder="ornek@firma.com"
            />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="password">Şifre</label>
            <input
              id="password"
              type="password"
              className="input"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
              autoComplete="current-password"
              placeholder="••••••••"
            />
            <div style={{ textAlign: 'right' }}>
              <Link href="/sifremi-unuttum" className="fs-sm" style={{ color: 'var(--color-text-secondary)' }}>
                Şifremi Unuttum
              </Link>
            </div>
          </div>
          <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={loading}>
            {loading ? 'Giriş yapılıyor...' : 'Giriş Yap'}
          </button>
        </form>

        <p className={styles.switchLink}>
          Hesabınız yok mu?{' '}
          <Link href="/uye-ol">Üye Ol</Link>
        </p>
      </div>
    </div>
  )
}
