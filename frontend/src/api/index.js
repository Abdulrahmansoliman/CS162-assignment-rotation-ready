// api/index.js
import { 
  getAccessToken, 
  clearTokens,
  refreshAccessToken,
} from '../features/auth/services/authservice.js'

// In production, VITE_API_URL should be set to the backend URL (e.g., https://rotation-ready-api.onrender.com)
// In development, we use Vite's proxy which forwards /api to localhost:5000
const API_BASE_URL = import.meta.env.VITE_API_URL 
  ? `${import.meta.env.VITE_API_URL}/api/v1`
  : "/api/v1"

const commonHeaders = {
  "Content-Type": "application/json",
}

/**
 * Check if the user is authenticated.
 * 
 * Attempts to fetch the current user's profile to verify authentication.
 * This is used to protect routes and determine if a user session is valid.
 * 
 * @returns {Promise<boolean>} True if authenticated, false otherwise
 */
export const checkAuth = async () => {
  try {
    await apiFetch('/user/me')
    return true
  } catch {
    return false
  }
}

/**
 * Core API fetch utility with automatic token refresh.
 * 
 * Handles all API requests with automatic JWT token management:
 * - Adds authentication headers automatically
 * - Detects expired tokens and refreshes them
 * - Retries failed requests once after token refresh
 * - Redirects to login on authentication failure
 * 
 * @param {string} endpoint - API endpoint path (e.g., '/user/me')
 * @param {Object} [options={}] - Fetch options
 * @param {string} [options.method] - HTTP method (GET, POST, PUT, DELETE)
 * @param {string} [options.body] - Request body (already stringified JSON)
 * @param {Object} [options.headers] - Additional headers to merge
 * @returns {Promise<Object>} Parsed JSON response
 * @throws {Error} If request fails or user is not authenticated
 */
export const apiFetch = async (endpoint, options = {}) => {
  const buildHeaders = (token, extraHeaders = {}) => ({
    ...commonHeaders,
    ...(token && { 'Authorization': `Bearer ${token}` }),
    ...extraHeaders,
  })

  let token = getAccessToken()

  let response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: buildHeaders(token, options.headers),
  })

  // Handle unauthorized / expired token
  if (response.status === 401) {
    let errorData = {}
    try {
      errorData = await response.json()
    } catch {
      errorData = {}
    }

    // If the access token is expired, try to refresh and retry once
    if (errorData.message === 'Token has expired.') {
      const newToken = await refreshAccessToken()
      if (newToken) {
        token = newToken
        response = await fetch(`${API_BASE_URL}${endpoint}`, {
          ...options,
          headers: buildHeaders(token, options.headers),
        })

        if (response.ok) {
          return response.json()
        }

        // If retry still fails, fall through to logout / error handling
      }
    }

    // If refresh failed or token invalid for another reason
    clearTokens()
    window.location.href = '/login'
    throw new Error(errorData.message || "Request failed")
  }

  if (!response.ok) {
    const data = await response.json().catch(() => ({}))
    throw new Error(data.message || "Request failed")
  }

  return response.json()
}

export { API_BASE_URL }