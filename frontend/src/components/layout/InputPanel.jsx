import { cn } from '@/lib/utils'

export function InputPanel({ className, children }) {
  return (
    <aside className={cn("w-80 border-r bg-background", className)}>
      <div className="h-full overflow-y-auto p-4 space-y-6">
        {children}
      </div>
    </aside>
  )
}
