'use client'

import { useState } from 'react'

export default function NewsletterForm({ className }: { className?: string }) {
  const [loading, setLoading] = useState(false)
  const [done, setDone] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    // Sahte bir istek animasyonu
    setTimeout(() => {
      setLoading(false)
      setDone(true)
    }, 1000)
  }

  if (done) {
    return (
      <div className={`text-success fw-600 ${className}`} style={{ padding: '10px 0' }}>
        ✓ E-posta adresiniz başarıyla kaydedildi!
      </div>
    )
  }

  return (
    <form className={className} onSubmit={handleSubmit}>
      <input
        type="email"
        className="input"
        placeholder="E-posta adresiniz"
        style={{ maxWidth: '280px' }}
        required
        disabled={loading}
      />
      <button type="submit" className="btn btn-primary" disabled={loading}>
        {loading ? 'Kaydediliyor...' : 'Bildir'}
      </button>
    </form>
  )
}
