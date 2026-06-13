'use client'

import type { Metadata } from 'next'
import DashboardLayout from '@/components/DashboardLayout'
import { useDashboardAuth } from '@/hooks/useDashboardAuth'
import { businesses, content } from '@/lib/api'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import Icon from '@/components/Icon'
import styles from './page.module.css'

export default function DashboardPage() {
  const { user, loading } = useDashboardAuth()
  const [myBusinesses, setMyBusinesses] = useState<any[]>([])
  const [heroBadge, setHeroBadge] = useState<string>('')

  useEffect(() => {
    if (user) {
      businesses.list().then(setMyBusinesses).catch(() => {})
    }
  }, [user])

  useEffect(() => {
    content.home().then((c) => setHeroBadge(c.hero_badge)).catch(() => {})
  }, [])

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

        {/* Dönem Uyarısı (dinamik — backend'den güncel program/tarih) */}
        {heroBadge && (
          <div className="alert alert-info" style={{ marginBottom: '24px', display: 'flex', gap: '10px', alignItems: 'flex-start' }}>
            <Icon name="info" size={18} style={{ marginTop: '2px' }} />
            <span><strong>{heroBadge}.</strong> İşletmenizi ekleyip uygunluk kontrolü yapın.</span>
          </div>
        )}

        {/* İşletmeler */}
        {myBusinesses.length === 0 ? (
          <div className={styles.emptyState}>
            <div className={styles.emptyIcon}><Icon name="building" size={40} strokeWidth={1.5} /></div>
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
                <div className={styles.bizIcon}><Icon name="building" size={22} /></div>
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
