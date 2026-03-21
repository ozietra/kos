'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { tokenHelpers } from '@/lib/api'
import styles from './DashboardSidebar.module.css'

const NAV = [
  { href: '/dashboard', label: 'Ana Sayfa', icon: '⊞' },
]

export default function DashboardSidebar() {
  const path = usePathname()

  function handleLogout() {
    tokenHelpers.remove()
    window.location.href = '/'
  }

  return (
    <aside className={styles.sidebar}>
      <Link href="/" className={styles.logo}>
        kosgeb<span>hibe</span>.com
      </Link>

      <nav className={styles.nav}>
        <div className="label" style={{ marginBottom: '8px' }}>Kontrol Paneli</div>
        {NAV.map(item => (
          <Link
            key={item.href}
            href={item.href}
            className={`${styles.navItem} ${path === item.href ? styles.active : ''}`}
          >
            <span className={styles.icon}>{item.icon}</span>
            {item.label}
          </Link>
        ))}
      </nav>

      <div className={styles.bottom}>
        <button onClick={handleLogout} className={styles.logoutBtn}>
          Çıkış Yap
        </button>
      </div>
    </aside>
  )
}
