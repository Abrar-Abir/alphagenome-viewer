import { useState } from 'react'
import { Eye, EyeOff, Loader2 } from 'lucide-react'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { submitApiKey } from '@/lib/api'

export function ApiKeySetupDialog({ open, onConfigured }) {
  const [apiKey, setApiKey] = useState('')
  const [showKey, setShowKey] = useState(false)
  const [isValidating, setIsValidating] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async () => {
    if (!apiKey.trim()) return
    setIsValidating(true)
    setError(null)
    try {
      await submitApiKey(apiKey.trim())
      onConfigured()
    } catch (err) {
      const message =
        err.response?.data?.detail || err.message || 'Failed to validate API key'
      setError(message)
    } finally {
      setIsValidating(false)
    }
  }

  return (
    <Dialog open={open}>
      <DialogContent
        className="sm:max-w-md"
        onPointerDownOutside={(e) => e.preventDefault()}
        onEscapeKeyDown={(e) => e.preventDefault()}
      >
        <img src="/logo.png" alt="AlphaGenome Viewer" className="h-16 mx-auto" />
        <DialogHeader>
          <DialogTitle>Welcome to AlphaGenome Viewer</DialogTitle>
          <DialogDescription>
            Enter your AlphaGenome API key to get started. If you don't have one,
            you can{' '}
            <a
              href="https://deepmind.google.com/science/alphagenome/account/settings"
              target="_blank"
              rel="noopener noreferrer"
              className="underline text-primary"
            >
              get a free API key for non-commercial use here
            </a>
            .
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="api-key">API Key</Label>
            <div className="relative">
              <Input
                id="api-key"
                type={showKey ? 'text' : 'password'}
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="Enter your AlphaGenome API key"
                className="pr-10"
                disabled={isValidating}
                onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
              />
              <Button
                variant="ghost"
                size="icon"
                className="absolute right-0 top-0 h-10 w-10"
                onClick={() => setShowKey(!showKey)}
                type="button"
              >
                {showKey ? (
                  <EyeOff className="h-4 w-4" />
                ) : (
                  <Eye className="h-4 w-4" />
                )}
              </Button>
            </div>
          </div>

          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <Button
            onClick={handleSubmit}
            disabled={!apiKey.trim() || isValidating}
            className="w-full"
          >
            {isValidating ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Validating...
              </>
            ) : (
              'Save API Key'
            )}
          </Button>

          <p className="text-xs text-muted-foreground text-center">
            The first prediction may take longer as the model initializes.
          </p>
        </div>
      </DialogContent>
    </Dialog>
  )
}
