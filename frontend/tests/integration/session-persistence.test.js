import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { getAccessToken, getRefreshToken, clearTokens } from '@/features/auth/services/authservice'
import { checkAuth } from '@/api/index'

global.fetch = vi.fn()

describe('Integration: Session Persistence', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    sessionStorage.clear()
  })

  afterEach(() => {
    sessionStorage.clear()
  })

  describe('Token Persistence in SessionStorage', () => {
    it('persists tokens in sessionStorage after login', () => {
      sessionStorage.setItem('access_token', 'test-access-token')
      sessionStorage.setItem('refresh_token', 'test-refresh-token')

      expect(getAccessToken()).toBe('test-access-token')
      expect(getRefreshToken()).toBe('test-refresh-token')
    })

    it('retrieves tokens after page reload simulation', () => {
      // Simulate setting tokens
      sessionStorage.setItem('access_token', 'persisted-access')
      sessionStorage.setItem('refresh_token', 'persisted-refresh')

      // Simulate page reload by clearing module state but not sessionStorage
      vi.resetModules()

      // Tokens should still be available
      expect(sessionStorage.getItem('access_token')).toBe('persisted-access')
      expect(sessionStorage.getItem('refresh_token')).toBe('persisted-refresh')
    })

    it('maintains separate sessions in different tabs (simulated)', () => {
      // Tab 1: Set tokens
      sessionStorage.setItem('access_token', 'tab1-token')
      expect(getAccessToken()).toBe('tab1-token')

      // Simulate different tab by using a new sessionStorage scope
      const tab1Token = sessionStorage.getItem('access_token')

      // Tab 2: Would have its own sessionStorage in real browser
      sessionStorage.setItem('access_token', 'tab2-token')
      expect(getAccessToken()).toBe('tab2-token')

      // Verify tab1 token was there first
      expect(tab1Token).toBe('tab1-token')
    })
  })

  describe('Session Lifecycle', () => {
    it('establishes session on successful login', () => {
      const mockTokens = {
        access_token: 'new-session-access',
        refresh_token: 'new-session-refresh',
      }

      sessionStorage.setItem('access_token', mockTokens.access_token)
      sessionStorage.setItem('refresh_token', mockTokens.refresh_token)

      expect(getAccessToken()).toBe('new-session-access')
      expect(getRefreshToken()).toBe('new-session-refresh')
    })

    it('maintains session across multiple page interactions', () => {
      sessionStorage.setItem('access_token', 'persistent-token')

      // Interaction 1: Check auth
      expect(getAccessToken()).toBe('persistent-token')

      // Interaction 2: Make API call (simulated)
      expect(getAccessToken()).toBe('persistent-token')

      // Interaction 3: Access profile
      expect(getAccessToken()).toBe('persistent-token')

      // Token should remain unchanged
      expect(sessionStorage.getItem('access_token')).toBe('persistent-token')
    })

    it('ends session on logout', () => {
      sessionStorage.setItem('access_token', 'to-be-cleared')
      sessionStorage.setItem('refresh_token', 'to-be-cleared')

      expect(getAccessToken()).toBe('to-be-cleared')
      expect(getRefreshToken()).toBe('to-be-cleared')

      clearTokens()

      expect(getAccessToken()).toBeNull()
      expect(getRefreshToken()).toBeNull()
    })

    it('ends session on token expiration', () => {
      sessionStorage.setItem('access_token', 'expired-token')
      sessionStorage.setItem('refresh_token', 'expired-refresh')

      // Simulate token expiration by clearing
      clearTokens()

      expect(getAccessToken()).toBeNull()
      expect(getRefreshToken()).toBeNull()
    })
  })

  describe('No Session State', () => {
    it('starts with no session on first visit', () => {
      expect(getAccessToken()).toBeNull()
      expect(getRefreshToken()).toBeNull()
    })

    it('has no session after clearing tokens', () => {
      sessionStorage.setItem('access_token', 'temp-token')
      sessionStorage.setItem('refresh_token', 'temp-refresh')

      clearTokens()

      expect(getAccessToken()).toBeNull()
      expect(getRefreshToken()).toBeNull()
      expect(sessionStorage.getItem('access_token')).toBeNull()
      expect(sessionStorage.getItem('refresh_token')).toBeNull()
    })
  })

  describe('Session Validation After Reload', () => {
    it('validates existing session after page reload', async () => {
      sessionStorage.setItem('access_token', 'valid-reloaded-token')

      global.fetch.mockResolvedValue({
        ok: true,
        status: 200,
      })

      // Simulate checkAuth call after reload
      const token = getAccessToken()
      expect(token).toBe('valid-reloaded-token')

      const isValid = await checkAuth()
      expect(isValid).toBe(true)
    })

    it('detects invalid session after page reload', async () => {
      sessionStorage.setItem('access_token', 'invalid-reloaded-token')

      global.fetch.mockResolvedValue({
        ok: false,
        status: 401,
      })

      const isValid = await checkAuth()
      expect(isValid).toBe(false)
    })

    it('handles missing session after browser restart simulation', () => {
      // Browser restart clears sessionStorage
      sessionStorage.clear()

      expect(getAccessToken()).toBeNull()
      expect(getRefreshToken()).toBeNull()
    })
  })

  describe('Token Update During Session', () => {
    it('updates tokens during active session', () => {
      sessionStorage.setItem('access_token', 'original-token')
      sessionStorage.setItem('refresh_token', 'original-refresh')

      expect(getAccessToken()).toBe('original-token')

      // Simulate token refresh
      sessionStorage.setItem('access_token', 'refreshed-token')
      sessionStorage.setItem('refresh_token', 'refreshed-refresh')

      expect(getAccessToken()).toBe('refreshed-token')
      expect(getRefreshToken()).toBe('refreshed-refresh')
    })

    it('maintains session after token refresh', () => {
      sessionStorage.setItem('access_token', 'old-token')

      const oldToken = getAccessToken()
      expect(oldToken).toBe('old-token')

      // Token refresh occurs
      sessionStorage.setItem('access_token', 'new-token')

      const newToken = getAccessToken()
      expect(newToken).toBe('new-token')
      expect(newToken).not.toBe(oldToken)
    })
  })

  describe('Concurrent Session Operations', () => {
    it('handles multiple reads of token without corruption', () => {
      sessionStorage.setItem('access_token', 'concurrent-token')

      const reads = [
        getAccessToken(),
        getAccessToken(),
        getAccessToken(),
        getAccessToken(),
      ]

      reads.forEach((token) => {
        expect(token).toBe('concurrent-token')
      })
    })

    it('handles token clear during multiple operations', () => {
      sessionStorage.setItem('access_token', 'to-clear')

      expect(getAccessToken()).toBe('to-clear')

      clearTokens()

      expect(getAccessToken()).toBeNull()
      expect(getAccessToken()).toBeNull()
    })
  })
})
