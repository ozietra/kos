/**
 * Profesyonel tek renkli SVG ikon seti (emoji yerine).
 * `currentColor` kullanır; renk ve boyut CSS/prop ile kontrol edilir.
 */
import type { CSSProperties } from 'react'

type IconName =
  | 'info' | 'building' | 'document' | 'clipboard' | 'gear'
  | 'checkCircle' | 'xCircle' | 'spark' | 'arrowRight' | 'check'

const PATHS: Record<IconName, React.ReactNode> = {
  info: (
    <>
      <circle cx="12" cy="12" r="9" />
      <line x1="12" y1="11" x2="12" y2="16" />
      <circle cx="12" cy="7.5" r="0.6" fill="currentColor" stroke="none" />
    </>
  ),
  building: (
    <>
      <rect x="4" y="3" width="16" height="18" rx="1" />
      <line x1="8" y1="7" x2="10" y2="7" /><line x1="14" y1="7" x2="16" y2="7" />
      <line x1="8" y1="11" x2="10" y2="11" /><line x1="14" y1="11" x2="16" y2="11" />
      <line x1="8" y1="15" x2="10" y2="15" /><line x1="14" y1="15" x2="16" y2="15" />
      <line x1="11" y1="21" x2="13" y2="21" />
    </>
  ),
  document: (
    <>
      <path d="M6 2h8l4 4v16H6z" />
      <path d="M14 2v4h4" />
      <line x1="9" y1="13" x2="15" y2="13" /><line x1="9" y1="17" x2="15" y2="17" />
    </>
  ),
  clipboard: (
    <>
      <rect x="6" y="4" width="12" height="18" rx="1" />
      <rect x="9" y="2" width="6" height="4" rx="1" />
      <line x1="9" y1="11" x2="15" y2="11" /><line x1="9" y1="15" x2="15" y2="15" />
    </>
  ),
  gear: (
    <>
      <circle cx="12" cy="12" r="3" />
      <path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9 17 7M7 17l-2.1 2.1" />
    </>
  ),
  checkCircle: (
    <>
      <circle cx="12" cy="12" r="9" />
      <path d="M8 12.5l2.5 2.5L16 9.5" />
    </>
  ),
  xCircle: (
    <>
      <circle cx="12" cy="12" r="9" />
      <line x1="9" y1="9" x2="15" y2="15" /><line x1="15" y1="9" x2="9" y2="15" />
    </>
  ),
  spark: (
    <>
      <path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z" />
    </>
  ),
  arrowRight: (
    <>
      <line x1="4" y1="12" x2="19" y2="12" /><path d="M13 6l6 6-6 6" />
    </>
  ),
  check: (
    <>
      <path d="M5 12.5l4 4L19 7" />
    </>
  ),
}

interface Props {
  name: IconName
  size?: number
  strokeWidth?: number
  style?: CSSProperties
  className?: string
}

export default function Icon({ name, size = 20, strokeWidth = 1.8, style, className }: Props) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={strokeWidth}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      style={{ flexShrink: 0, ...style }}
      className={className}
    >
      {PATHS[name]}
    </svg>
  )
}
