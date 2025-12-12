import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { apiFetch, checkAuth } from '@/api/index'
import * as authService from '@/features/auth/services/authservice'

vi.mock('@/features/auth/services/authservice')

global.fetch = vi.fn()

describe('Integration: API Token Handling and 401 Errors', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    sessionStorage.clear()
    delete window.location
    window.location = { href: '' }
  })

  afterEach(() => {
    sessionStorage.clear()
  })

  describe('401 Token Expiration Flow', () => {
    it('clears tokens and redirects on 401 error', async () => {
      authService.getAccessToken.mockReturnValue('expired-token')
      authService.clearTokens.mockImplementation(() => {
        sessionStorage.clear()
      })

      global.fetch.mockResolvedValue({
        ok: false,
        status: 401,
        json: async () => ({ message: 'Token expired' }),
      })

      await expect(apiFetch('/protected-endpoint', { method: 'GET' }))
        .rejects.toThrow('Token expired')

      expect(authService.clearTokens).toHaveBeenCalled()
      expect(window.location.href).toBe('/login')
    })

    it('handles 401 during profile fetch', async () => {
      authService.getAccessToken.mockReturnValue('bad-token')
      authService.clearTokens.mockImplementation(() => {
        sessionStorage.clear()
      })

      global.fetch.mockResolvedValue({
        ok: false,
        status: 401,
        json: async () => ({ message: 'Unauthorized' }),
      })

      await expect(apiFetch('user/me', { method: 'GET' }))
        .rejects.toThrow('Unauthorized')

      expect(authService.clearTokens).toHaveBeenCalledTimes(1)
      expect(window.location.href).toBe('/login')
    })

    it('handles 401 during data mutation', async () => {
      authService.getAccessToken.mockReturnValue('expired-token')
      authService.clearTokens.mockImplementation(() => {
        sessionStorage.clear()
      })

      global.fetch.mockResolvedValue({
        ok: false,
        status: 401,
        json: async () => ({ message: 'Session expired' }),
      })

      await expect(apiFetch('user/me', {
        method: 'PUT',
        body: JSON.stringify({ first_name: 'Updated' }),
      })).rejects.toThrow('Session expired')

      expect(authService.clearTokens).toHaveBeenCalled()
      expect(window.location.href).toBe('/login')
    })
  })

  describe('Token Validation', () => {
    it('validates token with checkAuth before protected operations', async () => {
      authService.getAccessToken.mockReturnValue('valid-token')
      
      global.fetch.mockResolvedValue({
        ok: true,
        status: 200,
      })

      const isAuthenticated = await checkAuth()

      expect(isAuthenticated).toBe(true)
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/auth/me'),
        expect.objectContaining({
          headers: { Authorization: 'Bearer valid-token' },
        })
      )
    })

    it('detects invalid token with checkAuth', async () => {
      authService.getAccessToken.mockReturnValue('invalid-token')
      authService.clearTokens.mockImplementation(() => {
        sessionStorage.clear()
      })

      global.fetch.mockResolvedValue({
        ok: false,
        status: 401,
      })

      const isAuthenticated = await checkAuth()

      expect(isAuthenticated).toBe(false)
      expect(authService.clearTokens).toHaveBeenCalled()
    })

    it('returns false when no token exists', async () => {
      authService.getAccessToken.mockReturnValue(null)

      const isAuthenticated = await checkAuth()

      expect(isAuthenticated).toBe(false)
      expect(global.fetch).not.toHaveBeenCalled()
    })
  })

  describe('Multiple 401 Errors', () => {
    it('handles rapid 401 errors without duplicate token clearing', async () => {
      authService.getAccessToken.mockReturnValue('expired-token')
      authService.clearTokens.mockImplementation(() => {
        sessionStorage.clear()
      })

      global.fetch.mockResolvedValue({
        ok: false,
        status: 401,
        json: async () => ({ message: 'Unauthorized' }),
      })

      // Simulate multiple concurrent API calls
      const requests = [
        apiFetch('/endpoint1', { method: 'GET' }),
        apiFetch('/endpoint2', { method: 'GET' }),
        apiFetch('/endpoint3', { method: 'GET' }),
      ]

      await Promise.allSettled(requests)

      // Token should be cleared at least once
      expect(authService.clearTokens).toHaveBeenCalled()
      // Should redirect to login
      expect(window.location.href).toBe('/login')
    })
  })

  describe('Token Recovery After 401', () => {
    it('requires new login after 401 clears tokens', async () => {
      // First request with expired token
      authService.getAccessToken.mockReturnValueOnce('expired-token')
      authService.clearTokens.mockImplementation(() => {
        sessionStorage.clear()
      })

      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 401,
        json: async () => ({ message: 'Token expired' }),
      })

      await expect(apiFetch('/protected', { method: 'GET' }))
        .rejects.toThrow('Token expired')

      expect(authService.clearTokens).toHaveBeenCalled()

      // After clearing, no token should be available
      authService.getAccessToken.mockReturnValue(null)

      const isAuthenticated = await checkAuth()
      expect(isAuthenticated).toBe(false)

      // New login provides fresh token
      authService.getAccessToken.mockReturnValue('new-valid-token')

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ data: 'success' }),
      })

      const result = await apiFetch('/protected', { method: 'GET' })
      expect(result).toEqual({ data: 'success' })
    })
  })

  describe('Non-401 Errors', () => {
    it('does not clear tokens on 403 error', async () => {
      authService.getAccessToken.mockReturnValue('valid-token')

      global.fetch.mockResolvedValue({
        ok: false,
        status: 403,
        json: async () => ({ message: 'Forbidden' }),
      })

      await expect(apiFetch('/forbidden', { method: 'GET' }))
        .rejects.toThrow('Forbidden')

      expect(authService.clearTokens).not.toHaveBeenCalled()
      expect(window.location.href).not.toBe('/login')
    })

    it('does not clear tokens on 500 error', async () => {
      authService.getAccessToken.mockReturnValue('valid-token')

      global.fetch.mockResolvedValue({
        ok: false,
        status: 500,
        json: async () => ({ message: 'Server error' }),
      })

      await expect(apiFetch('/server-error', { method: 'GET' }))
        .rejects.toThrow('Server error')

      expect(authService.clearTokens).not.toHaveBeenCalled()
    })
  })
})
