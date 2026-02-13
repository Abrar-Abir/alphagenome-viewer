import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
})

// --- API key localStorage helpers ---
const API_KEY_STORAGE_KEY = 'alphagenome_api_key'
export const getStoredApiKey = () => localStorage.getItem(API_KEY_STORAGE_KEY)
export const setStoredApiKey = (key) => localStorage.setItem(API_KEY_STORAGE_KEY, key)
export const clearStoredApiKey = () => localStorage.removeItem(API_KEY_STORAGE_KEY)

// Attach API key header to every request
api.interceptors.request.use((config) => {
  const apiKey = getStoredApiKey()
  if (apiKey) {
    config.headers['X-API-Key'] = apiKey
  }
  return config
})

// On 401 responses, clear the stored key so the setup dialog re-appears
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      clearStoredApiKey()
    }
    return Promise.reject(error)
  },
)

export const fetchOutputTypes = async () => {
  const { data } = await api.get('/api/metadata/output-types')
  return data.output_types
}

export const fetchOntologyTerms = async (search = '') => {
  const params = search ? { search } : {}
  const { data } = await api.get('/api/metadata/ontology-terms', { params })
  return data.terms
}

export const predictInterval = async (request) => {
  const { data } = await api.post('/api/predict/interval', request)
  return data
}

export const predictVariant = async (request) => {
  const { data } = await api.post('/api/predict/variant', request)
  return data
}

export const scoreVariant = async (request) => {
  const { data } = await api.post('/api/score/variant', request)
  return data
}

export const checkHealth = async () => {
  const { data } = await api.get('/health')
  return data
}

export const submitApiKey = async (apiKey) => {
  const { data } = await api.post('/api/config/api-key', { api_key: apiKey })
  setStoredApiKey(apiKey)
  return data
}

export default api
