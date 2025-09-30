// API configuration
// Prefer explicit env var; otherwise, derive from current window location so deployed hosts work
const API_BASE_URL =
  import.meta.env.VITE_API_URL ||
  (typeof window !== 'undefined'
    ? `${window.location.protocol}//${window.location.hostname}:8000`
    : 'http://localhost:8000')

console.log('API Base URL:', API_BASE_URL)

export const config = {
  apiBaseUrl: API_BASE_URL,
}