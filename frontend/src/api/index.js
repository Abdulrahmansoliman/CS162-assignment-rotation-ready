import { getAccessToken, clearTokens } from '../features/auth/services/authservice.js'

// In production, VITE_API_URL should be set to the backend URL (e.g., https://rotation-ready-api.onrender.com)
// In development, we use Vite's proxy which forwards /api to localhost:5000
const API_BASE_URL = import.meta.env.VITE_API_URL 
  ? `${import.meta.env.VITE_API_URL}/api/v1`
  : "/api/v1"

const commonHeaders = {
  "Content-Type": "application/json",
}

export const checkAuth = async () => {
  try {
    const token = getAccessToken()
    if (!token) return false
    
    const response = await fetch(`${API_BASE_URL}/user/me`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (response.status === 401) {
      clearTokens()
      return false
    }
    
    return response.ok 
  } catch {
    return false
  }
}

export const apiFetch = async (endpoint, options = {}) => {
  const token = getAccessToken()
  
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      ...commonHeaders,
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    },
  })

  if (!response.ok) {
    const data = await response.json()
    
    if (response.status === 401) {
      clearTokens()
      window.location.href = '/login' 
    }
    
    throw new Error(data.message || "Request failed")
  }

  return response.json()
}

export { API_BASE_URL }