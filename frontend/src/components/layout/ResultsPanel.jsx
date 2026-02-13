import { cn } from '@/lib/utils'

export function ResultsPanel({ className, children }) {
  return (
    <main className={cn("flex-1 bg-muted/20", className)}>
      <div className="h-full overflow-y-auto p-6">
        {children}
      </div>
    </main>
  )
}
