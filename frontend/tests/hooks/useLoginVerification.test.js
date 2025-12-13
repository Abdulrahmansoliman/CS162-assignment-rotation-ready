import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { useLoginVerification } from '@/features/auth/hooks/useLoginVerification'
import { authService } from '@/features/auth/services/authservice'

vi.mock('@/features/auth/services/authservice')
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom')
  return {
    ...actual,
    useNavigate: () => vi.fn(),
  }
})

describe('useLoginVerification', () => {
  const mockEmail = 'test@uni.minerva.edu'

  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('Initial State', () => {
    it('initializes with empty verification code', () => {
      const { result } = renderHook(() => useLoginVerification(mockEmail), {
        wrapper: BrowserRouter,
      })

      expect(result.current.verificationCode).toBe('')
      expect(result.current.errors).toEqual({})
      expect(result.current.isLoading).toBe(false)
      expect(result.current.isResending).toBe(false)
    })
  })

  describe('Verification Code Handling', () => {
    it('updates verification code with uppercase alphanumeric', () => {
      const { result } = renderHook(() => useLoginVerification(mockEmail), {
        wrapper: BrowserRouter,
      })

      act(() => {
        result.current.handleVerificationCodeChange('abc123')
      })

      expect(result.current.verificationCode).toBe('ABC123')
    })

    it('limits verification code to 6 characters', () => {
      const { result } = renderHook(() => useLoginVerification(mockEmail), {
        wrapper: BrowserRouter,
      })

      act(() => {
        result.current.handleVerificationCodeChange('abcdefghij')
      })

      expect(result.current.verificationCode).toBe('ABCDEF')
    })

    it('removes invalid characters from verification code', () => {
      const { result } = renderHook(() => useLoginVerification(mockEmail), {
        wrapper: BrowserRouter,
      })

      act(() => {
        result.current.handleVerificationCodeChange('a@b#c$1')
      })

      expect(result.current.verificationCode).toBe('ABC1')
    })
  })

  describe('Verification Submission', () => {
    it('submits verification code successfully', async () => {
      authService.verifyLogin.mockResolvedValue({})
      const { result } = renderHook(() => useLoginVerification(mockEmail), {
        wrapper: BrowserRouter,
      })

      act(() => {
        result.current.handleVerificationCodeChange('ABC123')
      })

      let submitResult
      await act(async () => {
        submitResult = await result.current.handleSubmit()
      })

      expect(submitResult.success).toBe(true)
      expect(authService.verifyLogin).toHaveBeenCalledWith({
        email: mockEmail,
        verificationCode: 'ABC123',
      })
    })

    it('handles verification error', async () => {
      authService.verifyLogin.mockRejectedValue(new Error('Invalid code'))
      const { result } = renderHook(() => useLoginVerification(mockEmail), {
        wrapper: BrowserRouter,
      })

      act(() => {
        result.current.handleVerificationCodeChange('ABC123')
      })

      let submitResult
      await act(async () => {
        submitResult = await result.current.handleSubmit()
      })

      expect(submitResult.success).toBe(false)
      expect(result.current.errors.submit).toBe('Invalid code')
    })
  })

  describe('Resend Code', () => {
    it('resends verification code successfully', async () => {
      authService.login.mockResolvedValue({})
      const { result } = renderHook(() => useLoginVerification(mockEmail), {
        wrapper: BrowserRouter,
      })

      await act(async () => {
        await result.current.handleResendCode()
      })

      expect(authService.login).toHaveBeenCalledWith({ email: mockEmail })
      expect(result.current.resendMessage).toContain('resent successfully')
    })

    it('handles resend error', async () => {
      authService.login.mockRejectedValue(new Error('Resend failed'))
      const { result } = renderHook(() => useLoginVerification(mockEmail), {
        wrapper: BrowserRouter,
      })

      await act(async () => {
        await result.current.handleResendCode()
      })

      expect(result.current.errors.submit).toBe('Resend failed')
    })
  })

  describe('Reset', () => {
    it('resets all state', () => {
      const { result } = renderHook(() => useLoginVerification(mockEmail), {
        wrapper: BrowserRouter,
      })

      act(() => {
        result.current.handleVerificationCodeChange('ABC123')
      })

      act(() => {
        result.current.reset()
      })

      expect(result.current.verificationCode).toBe('')
      expect(result.current.errors).toEqual({})
      expect(result.current.resendMessage).toBe('')
    })
  })
})
