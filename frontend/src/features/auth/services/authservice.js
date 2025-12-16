// authservice.js
import { apiFetch, API_BASE_URL } from "../../../api/index.js"

const AUTH_PREFIX = "/auth"

const saveTokens = (accessToken, refreshToken) => {
  localStorage.setItem('access_token', accessToken)
  localStorage.setItem('refresh_token', refreshToken)
}

export const getAccessToken = () => localStorage.getItem('access_token')
export const getRefreshToken = () => localStorage.getItem('refresh_token')

export const clearTokens = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
}

// NEW: refresh access token using the refresh token
export const refreshAccessToken = async () => {
  const refreshToken = getRefreshToken()
  if (!refreshToken) {
    clearTokens()
    return null
  }

  const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${refreshToken}`,
    },
  })

  if (!response.ok) {
    clearTokens()
    return null
  }

  const data = await response.json()
  const newAccessToken = data.access_token

  if (!newAccessToken) {
    clearTokens()
    return null
  }

  // Keep existing refresh token, just update access
  localStorage.setItem('access_token', newAccessToken)
  return newAccessToken
}

export const authService = {
  async register({ email, cityId, firstName, lastName }) {
    return apiFetch(`${AUTH_PREFIX}/register`, {
      method: "POST",
      body: JSON.stringify({
        email,
        city_id: parseInt(cityId),
        first_name: firstName,
        last_name: lastName,
      }),
    })
  },

  async verifyRegistration({ email, verificationCode }) {
    const response = await apiFetch(`${AUTH_PREFIX}/register/verify`, {
      method: "POST",
      body: JSON.stringify({
        email,
        verification_code: verificationCode,
      }),
    })
    
    saveTokens(response.access_token, response.refresh_token)
    return response
  },

  async resendVerificationCode({ email }) {
    return apiFetch(`${AUTH_PREFIX}/register/resend-code`, {
      method: "POST",
      body: JSON.stringify({ email }),
    })
  },

  async login({ email }) {
    return apiFetch(`${AUTH_PREFIX}/login`, {
      method: "POST",
      body: JSON.stringify({ email }),
    })
  },

  async verifyLogin({ email, verificationCode }) {
    const response = await apiFetch(`${AUTH_PREFIX}/login/verify`, {
      method: "POST",
      body: JSON.stringify({
        email,
        verification_code: verificationCode,
      }),
    })
    
    saveTokens(response.access_token, response.refresh_token)
    return response
  },

  async logout() {
    const response = await apiFetch(`${AUTH_PREFIX}/logout`, {
      method: "POST",
    })
    
    clearTokens()
    return response
  },
}