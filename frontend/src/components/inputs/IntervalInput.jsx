import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

const CHROMOSOMES = [
  'chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9', 'chr10',
  'chr11', 'chr12', 'chr13', 'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19',
  'chr20', 'chr21', 'chr22', 'chrX', 'chrY'
]

export function IntervalInput({ value, onChange, disabled }) {
  const width = value.end - value.start

  const handleChange = (field, val) => {
    onChange({ ...value, [field]: val })
  }

  return (
    <div className="space-y-3">
      <Label>Genomic Interval</Label>

      <Select
        value={value.chromosome}
        onValueChange={(val) => handleChange('chromosome', val)}
        disabled={disabled}
      >
        <SelectTrigger>
          <SelectValue placeholder="Select chromosome" />
        </SelectTrigger>
        <SelectContent>
          {CHROMOSOMES.map((chr) => (
            <SelectItem key={chr} value={chr}>
              {chr}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>

      <div className="grid grid-cols-2 gap-2">
        <div className="space-y-1">
          <Label className="text-xs text-muted-foreground">Start</Label>
          <Input
            type="number"
            value={value.start}
            onChange={(e) => handleChange('start', parseInt(e.target.value) || 0)}
            disabled={disabled}
            min={1}
          />
        </div>
        <div className="space-y-1">
          <Label className="text-xs text-muted-foreground">End</Label>
          <Input
            type="number"
            value={value.end}
            onChange={(e) => handleChange('end', parseInt(e.target.value) || 0)}
            disabled={disabled}
            min={1}
          />
        </div>
      </div>

      <p className="text-xs text-muted-foreground">
        Width: {width > 0 ? width.toLocaleString() : 0} bp
      </p>
    </div>
  )
}
