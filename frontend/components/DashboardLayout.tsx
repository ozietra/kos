import styles from './DashboardLayout.module.css'
import DashboardSidebar from './DashboardSidebar'

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className={styles.shell}>
      <DashboardSidebar />
      <main className={styles.main}>
        {children}
      </main>
    </div>
  )
}
