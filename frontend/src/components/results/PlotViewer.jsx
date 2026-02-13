import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { LoadingState } from './LoadingState'

export function PlotViewer({ plotUrls = [], isLoading, interval, variant }) {
  if (isLoading) {
    return <LoadingState />
  }

  if (plotUrls.length === 0) {
    return (
      <Card>
        <CardContent className="py-12 text-center">
          <p className="text-muted-foreground">
            Submit a prediction to see results
          </p>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-4">
      {interval && (
        <Card>
          <CardContent className="py-3">
            <p className="text-sm text-muted-foreground">
              <span className="font-medium">Region:</span>{' '}
              {interval.chromosome}:{interval.start.toLocaleString()}-{interval.end.toLocaleString()}{' '}
              ({interval.width.toLocaleString()} bp, {interval.sequence_length})
            </p>
          </CardContent>
        </Card>
      )}

      {variant && (
        <Card>
          <CardContent className="py-3">
            <p className="text-sm text-muted-foreground">
              <span className="font-medium">Variant:</span>{' '}
              {variant.chromosome}:{variant.position} {variant.ref}{'>'}{variant.alt}
            </p>
          </CardContent>
        </Card>
      )}

      {plotUrls.map((url, index) => {
        const outputType = url.split('_').pop()?.replace('.png', '')?.toUpperCase() || `Plot ${index + 1}`
        return (
          <Card key={url}>
            <CardHeader className="py-3">
              <CardTitle className="text-sm">{outputType}</CardTitle>
            </CardHeader>
            <CardContent>
              <img
                src={`${import.meta.env.VITE_API_BASE_URL || ''}${url}`}
                alt={`${outputType} prediction`}
                className="w-full rounded"
              />
            </CardContent>
          </Card>
        )
      })}
    </div>
  )
}
