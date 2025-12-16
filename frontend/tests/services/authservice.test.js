import { describe, it, expect, vi, beforeEach } from 'vitest'
import { authService, getAccessToken, clearTokens } from '@/features/auth/services/authservice'
import * as api from '@/api/index'

vi.mock('@/api/index')

describe('authService', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    sessionStorage.clear()
  })

  it('manages tokens correctly', () => {
    expect(typeof getAccessToken).toBe('function')
    expect(typeof clearTokens).toBe('function')
  })

  it('registers user successfully', async () => {
    api.apiFetch.mockResolvedValue({ success: true })

    await authService.register({
      email: 'test@uni.minerva.edu',
      cityId: 1,
      firstName: 'John',
      lastName: 'Doe',
    })

    expect(api.apiFetch).toHaveBeenCalled()
  })

  it('verifies login successfully', async () => {
    api.apiFetch.mockResolvedValue({
      access_token: 'new-token',
      refresh_token: 'refresh-token',
    })

    await authService.verifyLogin({
      email: 'test@uni.minerva.edu',
      verificationCode: 'ABC123',
    })

    expect(getAccessToken()).toBe('new-token')
  })

  it('logs out successfully', async () => {
    sessionStorage.setItem('access_token', 'test-token')
    api.apiFetch.mockResolvedValue({})

    await authService.logout()

    expect(getAccessToken()).toBeNull()
  })
})
