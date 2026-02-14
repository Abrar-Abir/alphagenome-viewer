import { useState, useMemo } from 'react'
import { Check, X, ChevronsUpDown } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Label } from '@/components/ui/label'
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/components/ui/command'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'

const ONTOLOGY_TERMS = [
  { name: 'Lung', code: 'UBERON:0002048', type: 'tissue' },
  { name: 'Brain', code: 'UBERON:0000955', type: 'tissue' },
  { name: 'Heart', code: 'UBERON:0000948', type: 'tissue' },
  { name: 'Liver', code: 'UBERON:0002107', type: 'tissue' },
  { name: 'Right liver lobe', code: 'UBERON:0001114', type: 'tissue' },
  { name: 'Kidney', code: 'UBERON:0002113', type: 'tissue' },
  { name: 'Colon - Transverse', code: 'UBERON:0001157', type: 'tissue' },
  { name: 'Stomach', code: 'UBERON:0000945', type: 'tissue' },
  { name: 'Pancreas', code: 'UBERON:0001264', type: 'tissue' },
  { name: 'Spleen', code: 'UBERON:0002106', type: 'tissue' },
  { name: 'Thyroid', code: 'UBERON:0002046', type: 'tissue' },
  { name: 'Skin', code: 'UBERON:0002097', type: 'tissue' },
  { name: 'Skeletal muscle', code: 'UBERON:0001134', type: 'tissue' },
  { name: 'Adipose tissue', code: 'UBERON:0001013', type: 'tissue' },
  { name: 'Blood', code: 'UBERON:0000178', type: 'tissue' },
  { name: 'Bone marrow', code: 'UBERON:0002371', type: 'tissue' },
  { name: 'K562 cell line', code: 'EFO:0002067', type: 'cell_line' },
  { name: 'HepG2 cell line', code: 'EFO:0001187', type: 'cell_line' },
  { name: 'GM12878 cell line', code: 'EFO:0002784', type: 'cell_line' },
]

export function OntologySelect({ selected, onChange, maxSelections = 5, disabled }) {
  const [open, setOpen] = useState(false)
  const [search, setSearch] = useState('')

  const terms = useMemo(() => {
    if (!search) return ONTOLOGY_TERMS
    const lower = search.toLowerCase()
    return ONTOLOGY_TERMS.filter(
      (t) => t.name.toLowerCase().includes(lower) || t.code.toLowerCase().includes(lower),
    )
  }, [search])

  const toggleTerm = (term) => {
    const exists = selected.some((t) => t.code === term.code)
    if (exists) {
      onChange(selected.filter((t) => t.code !== term.code))
    } else if (selected.length < maxSelections) {
      onChange([...selected, term])
    }
  }

  const removeTerm = (code) => {
    onChange(selected.filter((t) => t.code !== code))
  }

  return (
    <div className="space-y-3">
      <Label>Tissues / Cell Types</Label>

      {selected.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {selected.map((term) => (
            <Badge key={term.code} variant="secondary" className="gap-1">
              {term.name}
              <X
                className="h-3 w-3 cursor-pointer"
                onClick={() => removeTerm(term.code)}
              />
            </Badge>
          ))}
        </div>
      )}

      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            role="combobox"
            aria-expanded={open}
            className="w-full justify-between"
            disabled={disabled || selected.length >= maxSelections}
          >
            {selected.length >= maxSelections
              ? `Max ${maxSelections} selected`
              : 'Add tissue/cell type...'}
            <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-full p-0" align="start">
          <Command>
            <CommandInput
              placeholder="Search tissues..."
              value={search}
              onValueChange={setSearch}
            />
            <CommandList>
              <CommandEmpty>No tissue found.</CommandEmpty>
              <CommandGroup>
                {terms.map((term) => (
                  <CommandItem
                    key={term.code}
                    value={term.name}
                    onSelect={() => toggleTerm(term)}
                  >
                    <Check
                      className={`mr-2 h-4 w-4 ${
                        selected.some((t) => t.code === term.code)
                          ? 'opacity-100'
                          : 'opacity-0'
                      }`}
                    />
                    <span className="flex-1">{term.name}</span>
                    <span className="text-xs text-muted-foreground">
                      {term.code}
                    </span>
                  </CommandItem>
                ))}
              </CommandGroup>
            </CommandList>
          </Command>
        </PopoverContent>
      </Popover>

      <p className="text-xs text-muted-foreground">
        Select up to {maxSelections} tissues/cell types ({selected.length} selected)
      </p>
    </div>
  )
}
