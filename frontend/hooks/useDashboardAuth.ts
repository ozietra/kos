'use client'

import { useEffect, useState } from 'react'
import { auth, tokenHelpers } from '@/lib/api'
import { useRouter } from 'next/navigation'

const DEMO_USER = {
  id: 'demo-user-001',
  email: 'demo@kosgebhibe.com',
  name: 'Demo Kullanıcı',
  plan: 'starter',
  credits: 1,
}

export function useDashboardAuth() {
  const [user, setUser] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    async function check() {
      const token = tokenHelpers.get()
      if (!token) {
        router.replace('/giris')
        return
      }

      // Mock demo modu — backend olmadan dashboard görüntülemek için
      if (token === 'demo-token') {
        setUser(DEMO_USER)
        setLoading(false)
        return
      }

      try {
        const me = await auth.me()
        setUser(me)
      } catch {
        tokenHelpers.remove()
        router.replace('/giris')
      } finally {
        setLoading(false)
      }
    }
    check()
  }, [router])

  return { user, loading }
}
