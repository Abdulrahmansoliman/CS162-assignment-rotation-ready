// authservice.js
import { apiFetch, API_BASE_URL } from "../../../api/index.js"

const AUTH_PREFIX = "/auth"

/**
 * Save authentication tokens to localStorage.
 * 
 * Stores both access and refresh tokens for session persistence.
 * 
 * @param {string} accessToken - JWT access token
 * @param {string} refreshToken - JWT refresh token
 */
const saveTokens = (accessToken, refreshToken) => {
  localStorage.setItem('access_token', accessToken)
  localStorage.setItem('refresh_token', refreshToken)
}

/**
 * Retrieve the access token from localStorage.
 * 
 * @returns {string|null} Access token if exists, null otherwise
 */
export const getAccessToken = () => localStorage.getItem('access_token')

/**
 * Retrieve the refresh token from localStorage.
 * 
 * @returns {string|null} Refresh token if exists, null otherwise
 */
export const getRefreshToken = () => localStorage.getItem('refresh_token')

/**
 * Clear all authentication tokens from localStorage.
 * 
 * Used during logout or when tokens become invalid.
 */
export const clearTokens = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
}

/**
 * Refresh the access token using the refresh token.
 * 
 * Attempts to get a new access token when the current one expires.
 * Automatically clears tokens if refresh fails.
 * 
 * @returns {Promise<string|null>} New access token if successful, null if refresh fails
 */
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

/**
 * Authentication service object containing all auth-related methods.
 */
export const authService = {
  /**
   * Register a new user account.
   * 
   * Creates a new user and sends a verification code to their email.
   * 
   * @param {Object} params - Registration parameters
   * @param {string} params.email - User's email address
   * @param {number} params.cityId - Rotation city ID
   * @param {string} params.firstName - User's first name
   * @param {string} params.lastName - User's last name
   * @returns {Promise<Object>} Registration response with message
   * @throws {Error} If registration fails or email already exists
   */
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

  /**
   * Verify user registration with email verification code.
   * 
   * Confirms the user's email address and activates their account.
   * Automatically saves authentication tokens on success.
   * 
   * @param {Object} params - Verification parameters
   * @param {string} params.email - User's email address
   * @param {string} params.verificationCode - 6-digit verification code from email
   * @returns {Promise<Object>} Response with access_token and refresh_token
   * @throws {Error} If code is invalid or expired
   */
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

  /**
   * Resend verification code to user's email.
   * 
   * Request a new verification code if the previous one expired or was lost.
   * Subject to rate limiting.
   * 
   * @param {Object} params - Resend parameters
   * @param {string} params.email - User's email address
   * @returns {Promise<Object>} Response confirming code was sent
   * @throws {Error} If rate limit exceeded or email not found
   */
  async resendVerificationCode({ email }) {
    return apiFetch(`${AUTH_PREFIX}/register/resend-code`, {
      method: "POST",
      body: JSON.stringify({ email }),
    })
  },

  /**
   * Initiate passwordless login.
   * 
   * Sends a verification code to the user's email for authentication.
   * User must be already registered and verified.
   * 
   * @param {Object} params - Login parameters
   * @param {string} params.email - User's email address
   * @returns {Promise<Object>} Response confirming code was sent
   * @throws {Error} If user not found or not verified
   */
  async login({ email }) {
    return apiFetch(`${AUTH_PREFIX}/login`, {
      method: "POST",
      body: JSON.stringify({ email }),
    })
  },

  /**
   * Verify login with email verification code.
   * 
   * Completes the passwordless login flow by verifying the code.
   * Automatically saves authentication tokens on success.
   * 
   * @param {Object} params - Verification parameters
   * @param {string} params.email - User's email address
   * @param {string} params.verificationCode - 6-digit verification code from email
   * @returns {Promise<Object>} Response with access_token and refresh_token
   * @throws {Error} If code is invalid or expired
   */
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

  /**
   * Log out the current user.
   * 
   * Invalidates the user's session on the server and clears local tokens.
   * 
   * @returns {Promise<Object>} Logout confirmation response
   * @throws {Error} If logout request fails
   */
  async logout() {
    const response = await apiFetch(`${AUTH_PREFIX}/logout`, {
      method: "POST",
    })
    
    clearTokens()
    return response
  },
}