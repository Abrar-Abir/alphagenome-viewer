import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { AlertCircle } from 'lucide-react'

import { Header } from '@/components/layout/Header'
import { InputPanel } from '@/components/layout/InputPanel'
import { ResultsPanel } from '@/components/layout/ResultsPanel'
import { ApiKeySetupDialog } from '@/components/ApiKeySetupDialog'
import { ModeSelector } from '@/components/inputs/ModeSelector'
import { IntervalInput } from '@/components/inputs/IntervalInput'
import { VariantInput } from '@/components/inputs/VariantInput'
import { OutputTypeSelect } from '@/components/inputs/OutputTypeSelect'
import { OntologySelect } from '@/components/inputs/OntologySelect'
import { PlotViewer } from '@/components/results/PlotViewer'
import { DataTable } from '@/components/results/DataTable'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { predictInterval, predictVariant, scoreVariant, getStoredApiKey, clearStoredApiKey } from '@/lib/api'

function App() {
  const [apiKeyConfigured, setApiKeyConfigured] = useState(() => !!getStoredApiKey())
  const [mode, setMode] = useState('predict')
  const [interval, setInterval] = useState({
    chromosome: 'chr19',
    start: 40991281,
    end: 41018398,
  })
  const [variant, setVariant] = useState({
    chromosome: 'chr22',
    position: 36201698,
    ref: 'A',
    alt: 'C',
  })
  const [outputTypes, setOutputTypes] = useState(['RNA_SEQ'])
  const [ontologyTerms, setOntologyTerms] = useState([])

  // Result states
  const [plotUrls, setPlotUrls] = useState([])
  const [resultInterval, setResultInterval] = useState(null)
  const [resultVariant, setResultVariant] = useState(null)
  const [scores, setScores] = useState([])

  // Mutations
  const intervalMutation = useMutation({
    mutationFn: predictInterval,
    onSuccess: (data) => {
      setPlotUrls(data.plot_urls)
      setResultInterval(data.interval)
      setResultVariant(null)
      setScores([])
    },
  })

  const variantMutation = useMutation({
    mutationFn: predictVariant,
    onSuccess: (data) => {
      setPlotUrls(data.plot_urls)
      setResultInterval(data.interval)
      setResultVariant(data.variant)
      setScores([])
    },
  })

  const scoreMutation = useMutation({
    mutationFn: scoreVariant,
    onSuccess: (data) => {
      setPlotUrls([])
      setResultInterval(null)
      setResultVariant(data.variant)
      setScores(data.scores)
    },
  })

  const isLoading =
    intervalMutation.isPending ||
    variantMutation.isPending ||
    scoreMutation.isPending

  const error =
    intervalMutation.error || variantMutation.error || scoreMutation.error

  const handleSubmit = () => {
    const ontologyCodes = ontologyTerms.map((t) => t.code)

    if (mode === 'predict') {
      intervalMutation.mutate({
        chromosome: interval.chromosome,
        start: interval.start,
        end: interval.end,
        output_types: outputTypes,
        ontology_terms: ontologyCodes,
      })
    } else if (mode === 'variant') {
      variantMutation.mutate({
        chromosome: variant.chromosome,
        position: variant.position,
        ref: variant.ref,
        alt: variant.alt,
        output_types: outputTypes,
        ontology_terms: ontologyCodes,
      })
    } else if (mode === 'score') {
      scoreMutation.mutate({
        chromosome: variant.chromosome,
        position: variant.position,
        ref: variant.ref,
        alt: variant.alt,
        output_types: outputTypes,
      })
    }
  }

  const canSubmit =
    outputTypes.length > 0 &&
    (mode === 'predict'
      ? interval.chromosome && interval.start > 0 && interval.end > interval.start
      : variant.chromosome &&
        variant.position > 0 &&
        variant.ref &&
        variant.alt)

  return (
    <div className="h-screen flex flex-col">
      <ApiKeySetupDialog
        open={!apiKeyConfigured}
        onConfigured={() => setApiKeyConfigured(true)}
      />

      <Header onChangeApiKey={() => { clearStoredApiKey(); setApiKeyConfigured(false); }} />

      <div className="flex-1 flex overflow-hidden">
        <InputPanel>
          <ModeSelector value={mode} onChange={setMode} />

          {mode === 'predict' && (
            <IntervalInput value={interval} onChange={setInterval} />
          )}

          {(mode === 'variant' || mode === 'score') && (
            <VariantInput value={variant} onChange={setVariant} />
          )}

          <OutputTypeSelect
            selected={outputTypes}
            onChange={setOutputTypes}
          />

          {mode !== 'score' && (
            <OntologySelect
              selected={ontologyTerms}
              onChange={setOntologyTerms}
            />
          )}

          <Button
            onClick={handleSubmit}
            disabled={!canSubmit || isLoading}
            className="w-full"
          >
            {isLoading ? 'Processing...' : 'Submit'}
          </Button>

          {error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertTitle>Error</AlertTitle>
              <AlertDescription>
                {error.response?.data?.detail || error.message || 'An error occurred'}
              </AlertDescription>
            </Alert>
          )}
        </InputPanel>

        <ResultsPanel>
          {mode === 'score' ? (
            <DataTable
              data={scores}
              variant={resultVariant}
              isLoading={scoreMutation.isPending}
            />
          ) : (
            <PlotViewer
              plotUrls={plotUrls}
              interval={resultInterval}
              variant={resultVariant}
              isLoading={intervalMutation.isPending || variantMutation.isPending}
            />
          )}
        </ResultsPanel>
      </div>
    </div>
  )
}

export default App
