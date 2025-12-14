import { apiFetch } from "../../../api/index.js"

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