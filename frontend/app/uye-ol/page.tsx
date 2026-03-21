'use client'

import { useState, FormEvent } from 'react'
import Link from 'next/link'
import { auth, tokenHelpers } from '@/lib/api'
import styles from './../auth.module.css'

export default function UyeOlPage() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    if (password.length < 8) {
      setError('Şifre en az 8 karakter olmalıdır.')
      return
    }
    setLoading(true)
    try {
      await auth.register(email, password, name)
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
        <h1 className={styles.title}>Üye Ol</h1>
        <p className={styles.subtitle}>Ücretsiz uygunluk testi için kayıt gerekmez.</p>

        {error && <div className="alert alert-danger" style={{ marginBottom: '16px' }}>{error}</div>}

        <form onSubmit={handleSubmit} className={styles.form}>
          <div className="form-group">
            <label className="form-label" htmlFor="name">Ad Soyad (isteğe bağlı)</label>
            <input
              id="name"
              type="text"
              className="input"
              value={name}
              onChange={e => setName(e.target.value)}
              placeholder="Ali Veli"
              autoComplete="name"
            />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="email">E-posta</label>
            <input
              id="email"
              type="email"
              className="input"
              value={email}
              onChange={e => setEmail(e.target.value)}
              required
              placeholder="ornek@firma.com"
              autoComplete="email"
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
              placeholder="En az 8 karakter"
              autoComplete="new-password"
            />
          </div>
          <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={loading}>
            {loading ? 'Hesap oluşturuluyor...' : 'Üye Ol'}
          </button>
        </form>

        <p className={styles.legal}>
          Üye olarak <Link href="/kullanim-sartlari">Kullanım Şartları</Link>'nı ve{' '}
          <Link href="/kvkk">Aydınlatma Metni</Link>'ni kabul etmiş olursunuz.
        </p>

        <p className={styles.switchLink}>
          Zaten üye misiniz? <Link href="/giris">Giriş Yap</Link>
        </p>
      </div>
    </div>
  )
}
