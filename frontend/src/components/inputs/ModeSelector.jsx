import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { Label } from '@/components/ui/label'

const MODES = [
  { value: 'predict', label: 'Predict Interval', description: 'Predict outputs for a genomic region' },
  { value: 'variant', label: 'Variant Effects', description: 'Compare REF vs ALT predictions' },
  { value: 'score', label: 'Score Variant', description: 'Get quantified variant impact scores' },
]

export function ModeSelector({ value, onChange, disabled }) {
  return (
    <div className="space-y-3">
      <Label>Prediction Mode</Label>
      <RadioGroup value={value} onValueChange={onChange} disabled={disabled}>
        {MODES.map((mode) => (
          <div key={mode.value} className="flex items-start space-x-3">
            <RadioGroupItem value={mode.value} id={mode.value} className="mt-0.5" />
            <div className="space-y-0.5">
              <Label htmlFor={mode.value} className="font-normal cursor-pointer">
                {mode.label}
              </Label>
              <p className="text-xs text-muted-foreground">{mode.description}</p>
            </div>
          </div>
        ))}
      </RadioGroup>
    </div>
  )
}
