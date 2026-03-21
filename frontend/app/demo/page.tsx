'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import styles from './page.module.css'

/**
 * Demo Giriş Sayfası
 * Backend olmadan dashboard'u görüntülemek için 'demo-token' token'ı
 * localStorage'a yazar ve /dashboard'a yönlendirir.
 */
export default function DemoPage() {
  const router = useRouter()

  useEffect(() => {
    localStorage.setItem('token', 'demo-token')
    router.replace('/dashboard')
  }, [router])

  return (
    <div className={styles.wrap}>
      <div className={styles.card}>
        <div className={styles.spinner} />
        <p>Demo modu etkinleştiriliyor...</p>
      </div>
    </div>
  )
}
