import { describe, it, expect, vi, beforeEach } from 'vitest'
import { apiFetch, checkAuth, API_BASE_URL } from '@/api/index'
import * as authService from '@/features/auth/services/authservice'

vi.mock('@/features/auth/services/authservice')
global.fetch = vi.fn()

describe('API utilities', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    sessionStorage.clear()
  })

  it('checkAuth works with valid token', async () => {
    authService.getAccessToken.mockReturnValue('valid-token')
    global.fetch.mockResolvedValue({ 
      ok: true, 
      status: 200,
      json: async () => ({})
    })

    const result = await checkAuth()
    expect(result).toBe(true)
  })

  it('apiFetch makes requests successfully', async () => {
    authService.getAccessToken.mockReturnValue('test-token')
    global.fetch.mockResolvedValue({
      ok: true,
      json: async () => ({ data: 'success' }),
    })

    const result = await apiFetch('/test', { method: 'GET' })
    expect(result).toEqual({ data: 'success' })
  })
})
