'use client'

import type { Metadata } from 'next'
import DashboardLayout from '@/components/DashboardLayout'
import { useDashboardAuth } from '@/hooks/useDashboardAuth'
import { businesses, eligibility } from '@/lib/api'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import styles from './page.module.css'

export default function DashboardPage() {
  const { user, loading } = useDashboardAuth()
  const [myBusinesses, setMyBusinesses] = useState<any[]>([])

  useEffect(() => {
    if (user) {
      businesses.list().then(setMyBusinesses).catch(() => {})
    }
  }, [user])

  if (loading) {
    return (
      <DashboardLayout>
        <div className={styles.loadingScreen}>
          <div className={styles.spinner} />
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout>
      <div className={styles.page}>
        {/* Başlık */}
        <div className={styles.pageHeader}>
          <div>
            <h1 className={styles.pageTitle}>
              Hoş Geldiniz{user?.name ? `, ${user.name}` : ''}
            </h1>
            <p className="text-secondary">
              KOSGEB başvurunuzu hazırlamak için işletmenizi seçin veya yeni ekleyin.
            </p>
          </div>
          <Link href="/dashboard/isletme-ekle" className="btn btn-primary">
            + İşletme Ekle
          </Link>
        </div>

        {/* Dönem Uyarısı */}
        <div className="alert alert-warning" style={{ marginBottom: '24px' }}>
          <strong>📢 KOBİGEL + İGD başvuruları açık.</strong> Son başvuru tarihi: 30 Nisan 2026.
          İşletmenizi ekleyip uygunluk kontrolü yapın.
        </div>

        {/* İşletmeler */}
        {myBusinesses.length === 0 ? (
          <div className={styles.emptyState}>
            <div className={styles.emptyIcon}>🏢</div>
            <div className="card-title">Henüz işletme eklemediniz</div>
            <p className="text-secondary fs-sm" style={{ marginTop: '8px' }}>
              İşletme bilgilerinizi girerek uygunluk analizi başlatın.
            </p>
            <Link href="/dashboard/isletme-ekle" className="btn btn-primary" style={{ marginTop: '20px' }}>
              İlk İşletmemi Ekle
            </Link>
          </div>
        ) : (
          <div className={styles.businessGrid}>
            {myBusinesses.map(biz => (
              <Link key={biz.id} href={`/dashboard/isletme/${biz.id}`} className={styles.businessCard}>
                <div className={styles.bizIcon}>🏢</div>
                <div>
                  <div className="card-title">{biz.business_name}</div>
                  <div className="text-secondary fs-sm">
                    {biz.nace_code ? `NACE ${biz.nace_code}` : 'NACE kodu girilmemiş'}
                    {biz.city ? ` • ${biz.city}` : ''}
                  </div>
                </div>
                <div className={styles.bizArrow}>→</div>
              </Link>
            ))}
            <Link href="/dashboard/isletme-ekle" className={styles.addCard}>
              <span style={{ fontSize: '28px' }}>+</span>
              <span>İşletme Ekle</span>
            </Link>
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}
