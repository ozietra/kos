/** @type {import('next').NextConfig} */
const nextConfig = {
  // Next.js 16.2 App Router
  experimental: {
    // Faster prefetch (Next.js 16.2)
    prefetchInlining: true,
  },
  // API proxy: backend'e istekleri yönlendir
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/:path*`,
      },
    ]
  },
}

module.exports = nextConfig
