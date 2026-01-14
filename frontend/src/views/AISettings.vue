<template>
  <div class="max-w-4xl mx-auto space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-3xl font-bold">{{ t('nav.settings') }}</h2>
      <div class="flex items-center space-x-2">
        <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
        <span class="text-sm text-muted-foreground">Live</span>
      </div>
    </div>

    <!-- Provider Selection -->
    <Card>
      <CardHeader>
        <CardTitle>AI-Provider auswählen</CardTitle>
        <CardDescription>
          Wählen Sie Ihren bevorzugten AI-Provider und konfigurieren Sie die Einstellungen.
        </CardDescription>
      </CardHeader>
      <CardContent class="space-y-6">
        <!-- Provider Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="(provider, key) in providers"
            :key="key"
            class="border rounded-lg p-4 cursor-pointer transition-all hover:shadow-md hover:scale-105 active:scale-95 select-none"
            :class="{
              'border-primary bg-primary/10 ring-2 ring-primary/20': selectedProvider === key,
              'border-border hover:border-primary/50 hover:bg-accent/50': selectedProvider !== key
            }"
            @click="selectProvider(key)"
            @keydown.enter="selectProvider(key)"
            @keydown.space="selectProvider(key)"
            tabindex="0"
            role="button"
            :aria-pressed="selectedProvider === key"
          >
            <div class="flex items-center space-x-3 mb-2">
              <div class="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                <span class="text-sm font-semibold text-primary">
                  {{ provider.display_name.charAt(0) }}
                </span>
              </div>
              <div>
                <h3 class="font-semibold">{{ provider.display_name }}</h3>
                <p class="text-xs text-muted-foreground">{{ provider.pricing_info }}</p>
              </div>
            </div>
            <p class="text-sm text-muted-foreground mb-3">{{ provider.description }}</p>
            <div class="flex items-center justify-between">
              <span class="text-xs text-muted-foreground">{{ provider.website }}</span>
              <div class="flex items-center space-x-2">
                <div v-if="selectedProvider === provider.name" class="w-2 h-2 rounded-full bg-primary animate-pulse"></div>
                <div v-else class="w-2 h-2 rounded-full bg-muted"></div>
                <span v-if="selectedProvider === provider.name" class="text-xs text-primary font-medium">Ausgewählt</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Model Selection -->
        <div v-if="selectedProvider" class="space-y-4">
          <div>
            <Label for="model">Modell auswählen</Label>
            <select
              id="model"
              v-model="settings.ai_model"
              class="w-full mt-1 px-3 py-2 border border-input bg-background rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option v-for="model in currentProvider?.models" :key="model" :value="model">
                {{ model }}
              </option>
            </select>
          </div>

          <!-- API Key -->
          <div>
            <div class="flex items-center gap-2 mb-1">
              <Label for="api-key">API-Schlüssel</Label>
              <div v-if="hasApiKey" class="flex items-center gap-1 text-green-600">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
                <span class="text-xs font-medium">Gespeichert</span>
              </div>
            </div>
            <div class="flex space-x-2">
              <Input
                id="api-key"
                v-model="apiKey"
                type="password"
                :placeholder="hasApiKey ? '••••••••••••••••' : 'Ihr API-Schlüssel'"
                class="flex-1"
              />
              <Button @click="testConnection" :disabled="!apiKey || isTesting">
                <svg v-if="isTesting" class="w-4 h-4 animate-spin mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                </svg>
                <svg v-else class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                {{ isTesting ? 'Teste...' : 'Testen' }}
              </Button>
            </div>
            <p class="text-xs text-muted-foreground mt-1">
              {{ hasApiKey ? 'Ein API-Schlüssel ist gespeichert. Geben Sie einen neuen ein, um ihn zu ersetzen.' : 'Ihr API-Schlüssel wird verschlüsselt gespeichert und sicher übertragen.' }}
            </p>
          </div>

          <!-- Advanced Settings -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label for="temperature">Temperature ({{ settings.ai_temperature }})</Label>
              <input
                id="temperature"
                v-model.number="settings.ai_temperature"
                type="range"
                min="0"
                max="2"
                step="0.1"
                class="w-full mt-1"
              />
              <div class="flex justify-between text-xs text-muted-foreground mt-1">
                <span>Konservativ (0.0)</span>
                <span>Kreativ (2.0)</span>
              </div>
            </div>

            <div>
              <Label for="max-tokens">Max. Tokens</Label>
              <Input
                id="max-tokens"
                v-model.number="settings.ai_max_tokens"
                type="number"
                min="100"
                max="4000"
                step="100"
              />
              <p class="text-xs text-muted-foreground mt-1">
                Maximale Anzahl der generierten Tokens
              </p>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex justify-between pt-4">
            <Button variant="outline" @click="clearApiKey" :disabled="!hasApiKey">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
              </svg>
              API-Schlüssel löschen
            </Button>
            <Button @click="saveSettings" :disabled="isSaving">
              <svg v-if="isSaving" class="w-4 h-4 animate-spin mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
              </svg>
              <svg v-else class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
              </svg>
              {{ isSaving ? 'Speichere...' : 'Einstellungen speichern' }}
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Test Results -->
    <Card v-if="testResult">
      <CardHeader>
        <CardTitle class="flex items-center space-x-2">
          <div class="w-2 h-2 rounded-full" :class="testResult.success ? 'bg-green-500' : 'bg-red-500'"></div>
          <span>Verbindungstest</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p class="text-sm" :class="testResult.success ? 'text-green-600' : 'text-red-600'">
          {{ testResult.message }}
        </p>
        <p v-if="testResult.response" class="text-xs text-muted-foreground mt-2">
          Antwort: {{ testResult.response }}
        </p>
      </CardContent>
    </Card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

const { t } = useI18n()
const authStore = useAuthStore()

// Reactive data
const providers = ref({})
const selectedProvider = ref('')
const settings = ref({
  ai_provider: 'openai',
  ai_model: 'gpt-3.5-turbo',
  ai_temperature: 0.7,
  ai_max_tokens: 1000
})
const apiKey = ref('')
const hasApiKey = ref(false)
const isSaving = ref(false)
const isTesting = ref(false)
const testResult = ref(null)

// Computed
const currentProvider = computed(() => {
  return providers.value[selectedProvider.value]
})

// Methods
const loadProviders = async () => {
  try {
    const response = await fetch('/api/v1/ai-settings/providers')
    if (response.ok) {
      providers.value = await response.json()
    } else {
      // Fallback zu Mock-Daten wenn API nicht verfügbar
      providers.value = {
        "openai": {
          "name": "openai",
          "display_name": "OpenAI",
          "description": "OpenAI's GPT models including GPT-3.5 and GPT-4",
          "models": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o"],
          "default_model": "gpt-3.5-turbo",
          "website": "https://openai.com",
          "pricing_info": "Pay per token"
        },
        "deepseek": {
          "name": "deepseek",
          "display_name": "DeepSeek",
          "description": "Cost-effective AI models with competitive performance",
          "models": ["deepseek-chat", "deepseek-coder", "deepseek-math"],
          "default_model": "deepseek-chat",
          "website": "https://deepseek.com",
          "pricing_info": "Very affordable pricing"
        },
        "anthropic": {
          "name": "anthropic",
          "display_name": "Anthropic Claude",
          "description": "Anthropic's Claude models with strong reasoning capabilities",
          "models": ["claude-3-haiku", "claude-3-sonnet", "claude-3-opus"],
          "default_model": "claude-3-haiku",
          "website": "https://anthropic.com",
          "pricing_info": "Pay per token"
        },
        "google": {
          "name": "google",
          "display_name": "Google Gemini",
          "description": "Google's Gemini models with multimodal capabilities",
          "models": ["gemini-pro", "gemini-pro-vision"],
          "default_model": "gemini-pro",
          "website": "https://ai.google.dev",
          "pricing_info": "Pay per token"
        },
        "ollama": {
          "name": "ollama",
          "display_name": "Ollama (Local)",
          "description": "Run AI models locally on your machine",
          "models": ["llama2", "codellama", "mistral", "neural-chat"],
          "default_model": "llama2",
          "website": "https://ollama.ai",
          "pricing_info": "Free (local processing)"
        }
      }
    }
  } catch (error) {
    console.error('Failed to load providers:', error)
    // Fallback zu Mock-Daten
    providers.value = {
      "openai": {
        "name": "openai",
        "display_name": "OpenAI",
        "description": "OpenAI's GPT models including GPT-3.5 and GPT-4",
        "models": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o"],
        "default_model": "gpt-3.5-turbo",
        "website": "https://openai.com",
        "pricing_info": "Pay per token"
      },
      "deepseek": {
        "name": "deepseek",
        "display_name": "DeepSeek",
        "description": "Cost-effective AI models with competitive performance",
        "models": ["deepseek-chat", "deepseek-coder", "deepseek-math"],
        "default_model": "deepseek-chat",
        "website": "https://deepseek.com",
        "pricing_info": "Very affordable pricing"
      }
    }
  }
}

const loadSettings = async () => {
  try {
    const response = await fetch('/api/v1/ai-settings/', {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    
    if (response.ok) {
      const data = await response.json()
      settings.value = {
        ai_provider: data.ai_provider,
        ai_model: data.ai_model,
        ai_temperature: data.ai_temperature,
        ai_max_tokens: data.ai_max_tokens
      }
      selectedProvider.value = data.ai_provider
      hasApiKey.value = data.has_api_key
    }
  } catch (error) {
    console.error('Failed to load settings:', error)
  }
}

const selectProvider = (providerName) => {
  
  selectedProvider.value = providerName
  settings.value.ai_provider = providerName
  
  // Update model to default for selected provider
  const provider = providers.value[providerName]
  if (provider) {
    settings.value.ai_model = provider.default_model
  }
  
  // Clear previous test results when switching providers
  testResult.value = null
}

const testConnection = async () => {
  if (!apiKey.value) return
  
  isTesting.value = true
  testResult.value = null
  
  try {
    const response = await fetch('/api/v1/ai-settings/test-connection', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        ai_provider: selectedProvider.value,
        ai_model: settings.value.ai_model,
        ai_api_key: apiKey.value
      })
    })
    
    testResult.value = await response.json()
  } catch (error) {
    testResult.value = {
      success: false,
      message: 'Verbindungstest fehlgeschlagen',
      error: error.message
    }
  } finally {
    isTesting.value = false
  }
}

const saveSettings = async () => {
  isSaving.value = true
  
  try {
    const response = await fetch('/api/v1/ai-settings/', {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        ...settings.value,
        ai_api_key: apiKey.value || undefined
      })
    })
    
    if (response.ok) {
      await loadSettings() // Reload to get updated hasApiKey status
      apiKey.value = '' // Clear the input
    }
  } catch (error) {
    console.error('Failed to save settings:', error)
  } finally {
    isSaving.value = false
  }
}

const clearApiKey = async () => {
  try {
    const response = await fetch('/api/v1/ai-settings/api-key', {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    
    if (response.ok) {
      hasApiKey.value = false
      apiKey.value = ''
    }
  } catch (error) {
    console.error('Failed to clear API key:', error)
  }
}

// Lifecycle
onMounted(async () => {
  await loadProviders()
  await loadSettings()
})
</script>
