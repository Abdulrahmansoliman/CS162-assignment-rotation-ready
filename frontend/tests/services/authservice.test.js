import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { authService, getAccessToken, getRefreshToken, clearTokens } from '@/features/auth/services/authservice'
import * as api from '@/api/index'

vi.mock('@/api/index')

describe('authService', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    sessionStorage.clear()
  })

  afterEach(() => {
    sessionStorage.clear()
  })

  describe('Token Management', () => {
    it('stores tokens in sessionStorage', () => {
      sessionStorage.setItem('access_token', 'test-access-token')
      sessionStorage.setItem('refresh_token', 'test-refresh-token')

      expect(getAccessToken()).toBe('test-access-token')
      expect(getRefreshToken()).toBe('test-refresh-token')
    })

    it('clears tokens from sessionStorage', () => {
      sessionStorage.setItem('access_token', 'test-access-token')
      sessionStorage.setItem('refresh_token', 'test-refresh-token')

      clearTokens()

      expect(getAccessToken()).toBeNull()
      expect(getRefreshToken()).toBeNull()
    })
  })

  describe('register', () => {
    it('calls apiFetch with correct registration data', async () => {
      api.apiFetch.mockResolvedValue({ success: true })

      await authService.register({
        email: 'test@uni.minerva.edu',
        cityId: 1,
        firstName: 'John',
        lastName: 'Doe',
      })

      expect(api.apiFetch).toHaveBeenCalledWith('/auth/register', {
        method: 'POST',
        body: JSON.stringify({
          email: 'test@uni.minerva.edu',
          city_id: 1,
          first_name: 'John',
          last_name: 'Doe',
        }),
      })
    })

    it('converts cityId to integer', async () => {
      api.apiFetch.mockResolvedValue({ success: true })

      await authService.register({
        email: 'test@uni.minerva.edu',
        cityId: '2',
        firstName: 'John',
        lastName: 'Doe',
      })

      const callArgs = api.apiFetch.mock.calls[0]
      const body = JSON.parse(callArgs[1].body)
      expect(body.city_id).toBe(2)
      expect(typeof body.city_id).toBe('number')
    })
  })

  describe('verifyRegistration', () => {
    it('calls apiFetch and saves tokens', async () => {
      api.apiFetch.mockResolvedValue({
        access_token: 'new-access-token',
        refresh_token: 'new-refresh-token',
      })

      await authService.verifyRegistration({
        email: 'test@uni.minerva.edu',
        verificationCode: 'ABC123',
      })

      expect(api.apiFetch).toHaveBeenCalledWith('/auth/register/verify', {
        method: 'POST',
        body: JSON.stringify({
          email: 'test@uni.minerva.edu',
          verification_code: 'ABC123',
        }),
      })

      expect(getAccessToken()).toBe('new-access-token')
      expect(getRefreshToken()).toBe('new-refresh-token')
    })
  })

  describe('resendVerificationCode', () => {
    it('calls apiFetch with email', async () => {
      api.apiFetch.mockResolvedValue({ success: true })

      await authService.resendVerificationCode({
        email: 'test@uni.minerva.edu',
      })

      expect(api.apiFetch).toHaveBeenCalledWith('/auth/register/resend-code', {
        method: 'POST',
        body: JSON.stringify({ email: 'test@uni.minerva.edu' }),
      })
    })
  })

  describe('login', () => {
    it('calls apiFetch with email', async () => {
      api.apiFetch.mockResolvedValue({ success: true })

      await authService.login({ email: 'test@uni.minerva.edu' })

      expect(api.apiFetch).toHaveBeenCalledWith('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email: 'test@uni.minerva.edu' }),
      })
    })
  })

  describe('verifyLogin', () => {
    it('calls apiFetch and saves tokens', async () => {
      api.apiFetch.mockResolvedValue({
        access_token: 'login-access-token',
        refresh_token: 'login-refresh-token',
      })

      await authService.verifyLogin({
        email: 'test@uni.minerva.edu',
        verificationCode: 'XYZ789',
      })

      expect(api.apiFetch).toHaveBeenCalledWith('/auth/login/verify', {
        method: 'POST',
        body: JSON.stringify({
          email: 'test@uni.minerva.edu',
          verification_code: 'XYZ789',
        }),
      })

      expect(getAccessToken()).toBe('login-access-token')
      expect(getRefreshToken()).toBe('login-refresh-token')
    })
  })

  describe('logout', () => {
    it('calls apiFetch and clears tokens', async () => {
      sessionStorage.setItem('access_token', 'test-token')
      sessionStorage.setItem('refresh_token', 'test-refresh')
      api.apiFetch.mockResolvedValue({ success: true })

      await authService.logout()

      expect(api.apiFetch).toHaveBeenCalledWith('/auth/logout', {
        method: 'POST',
      })

      expect(getAccessToken()).toBeNull()
      expect(getRefreshToken()).toBeNull()
    })
  })
})
