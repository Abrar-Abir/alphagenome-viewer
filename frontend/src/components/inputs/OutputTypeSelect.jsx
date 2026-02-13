import { Checkbox } from '@/components/ui/checkbox'
import { Label } from '@/components/ui/label'

const OUTPUT_TYPES = [
  { value: 'RNA_SEQ', label: 'RNA-seq', description: 'Gene expression' },
  { value: 'DNASE', label: 'DNase-seq', description: 'Chromatin accessibility' },
  { value: 'ATAC', label: 'ATAC-seq', description: 'Chromatin accessibility' },
  { value: 'CAGE', label: 'CAGE', description: 'Transcription start sites' },
  { value: 'CHIP_HISTONE', label: 'ChIP (Histone)', description: 'Histone modifications' },
  { value: 'CHIP_TF', label: 'ChIP (TF)', description: 'Transcription factor binding' },
  { value: 'SPLICE_SITES', label: 'Splice Sites', description: 'Splice site predictions' },
  { value: 'SPLICE_SITE_USAGE', label: 'Splice Usage', description: 'Splice site usage' },
  { value: 'SPLICE_JUNCTIONS', label: 'Splice Junctions', description: 'Splice junctions' },
  { value: 'CONTACT_MAPS', label: 'Contact Maps', description: '3D chromatin contacts' },
  { value: 'PROCAP', label: 'PRO-cap', description: 'Nascent transcription' },
]

export function OutputTypeSelect({ selected, onChange, disabled }) {
  const toggle = (type) => {
    if (selected.includes(type)) {
      onChange(selected.filter((t) => t !== type))
    } else {
      onChange([...selected, type])
    }
  }

  return (
    <div className="space-y-2">
      <Label>Output Types</Label>
      <div className="grid grid-cols-2 gap-x-3 gap-y-1.5">
        {OUTPUT_TYPES.map((type) => (
          <div key={type.value} className="flex items-center space-x-1.5">
            <Checkbox
              id={type.value}
              checked={selected.includes(type.value)}
              onCheckedChange={() => toggle(type.value)}
              disabled={disabled}
            />
            <label
              htmlFor={type.value}
              className="text-xs cursor-pointer flex-1 leading-tight"
              title={type.description}
            >
              {type.label}
            </label>
          </div>
        ))}
      </div>
      <p className="text-xs text-muted-foreground">
        {selected.length} selected
      </p>
    </div>
  )
}
