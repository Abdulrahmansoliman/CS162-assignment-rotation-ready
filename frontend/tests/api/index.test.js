import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { apiFetch, checkAuth, API_BASE_URL } from '@/api/index'
import * as authService from '@/features/auth/services/authservice'

vi.mock('@/features/auth/services/authservice')

global.fetch = vi.fn()

describe('API utilities', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    sessionStorage.clear()
    delete window.location
    window.location = { href: '' }
  })

  afterEach(() => {
    sessionStorage.clear()
  })

  describe('checkAuth', () => {
    it('returns false when no token exists', async () => {
      authService.getAccessToken.mockReturnValue(null)

      const result = await checkAuth()

      expect(result).toBe(false)
    })

    it('returns true when token is valid', async () => {
      authService.getAccessToken.mockReturnValue('valid-token')
      global.fetch.mockResolvedValue({
        ok: true,
        status: 200,
      })

      const result = await checkAuth()

      expect(result).toBe(true)
      expect(global.fetch).toHaveBeenCalledWith(
        `${API_BASE_URL}/auth/me`,
        expect.objectContaining({
          headers: { Authorization: 'Bearer valid-token' },
        })
      )
    })

    it('clears tokens and returns false on 401', async () => {
      authService.getAccessToken.mockReturnValue('invalid-token')
      global.fetch.mockResolvedValue({
        ok: false,
        status: 401,
      })

      const result = await checkAuth()

      expect(result).toBe(false)
      expect(authService.clearTokens).toHaveBeenCalled()
    })

    it('returns false on fetch error', async () => {
      authService.getAccessToken.mockReturnValue('valid-token')
      global.fetch.mockRejectedValue(new Error('Network error'))

      const result = await checkAuth()

      expect(result).toBe(false)
    })
  })

  describe('apiFetch', () => {
    it('makes fetch request with correct URL and headers', async () => {
      authService.getAccessToken.mockReturnValue('test-token')
      global.fetch.mockResolvedValue({
        ok: true,
        json: async () => ({ data: 'success' }),
      })

      const result = await apiFetch('/test', { method: 'GET' })

      expect(global.fetch).toHaveBeenCalledWith(
        `${API_BASE_URL}/test`,
        expect.objectContaining({
          method: 'GET',
          headers: expect.objectContaining({
            'Content-Type': 'application/json',
            Authorization: 'Bearer test-token',
          }),
        })
      )
      expect(result).toEqual({ data: 'success' })
    })

    it('makes request without token when not authenticated', async () => {
      authService.getAccessToken.mockReturnValue(null)
      global.fetch.mockResolvedValue({
        ok: true,
        json: async () => ({ data: 'public' }),
      })

      await apiFetch('/public', { method: 'GET' })

      expect(global.fetch).toHaveBeenCalledWith(
        `${API_BASE_URL}/public`,
        expect.objectContaining({
          headers: expect.not.objectContaining({
            Authorization: expect.anything(),
          }),
        })
      )
    })

    it('throws error on failed request', async () => {
      authService.getAccessToken.mockReturnValue('test-token')
      global.fetch.mockResolvedValue({
        ok: false,
        status: 400,
        json: async () => ({ message: 'Bad request' }),
      })

      await expect(apiFetch('/test', { method: 'POST' })).rejects.toThrow('Bad request')
    })

    it('clears tokens and redirects on 401', async () => {
      authService.getAccessToken.mockReturnValue('expired-token')
      global.fetch.mockResolvedValue({
        ok: false,
        status: 401,
        json: async () => ({ message: 'Unauthorized' }),
      })

      await expect(apiFetch('/protected', { method: 'GET' })).rejects.toThrow('Unauthorized')

      expect(authService.clearTokens).toHaveBeenCalled()
      expect(window.location.href).toBe('/login')
    })

    it('includes custom headers in request', async () => {
      authService.getAccessToken.mockReturnValue('test-token')
      global.fetch.mockResolvedValue({
        ok: true,
        json: async () => ({ data: 'success' }),
      })

      await apiFetch('/test', {
        method: 'POST',
        headers: { 'X-Custom-Header': 'custom-value' },
      })

      expect(global.fetch).toHaveBeenCalledWith(
        `${API_BASE_URL}/test`,
        expect.objectContaining({
          headers: expect.objectContaining({
            'Content-Type': 'application/json',
            'X-Custom-Header': 'custom-value',
            Authorization: 'Bearer test-token',
          }),
        })
      )
    })
  })
})
