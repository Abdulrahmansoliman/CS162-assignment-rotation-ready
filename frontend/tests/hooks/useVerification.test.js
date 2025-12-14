import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { useVerification } from '@/features/auth/hooks/useVerification'
import { authService } from '@/features/auth/services/authservice'

vi.mock('@/features/auth/services/authservice')
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom')
  return {
    ...actual,
    useNavigate: () => vi.fn(),
  }
})

describe('useVerification', () => {
  const mockEmail = 'test@uni.minerva.edu'

  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('Initial State', () => {
    it('initializes with empty verification code', () => {
      const { result } = renderHook(() => useVerification(mockEmail), {
        wrapper: BrowserRouter,
      })

      expect(result.current.verificationCode).toBe('')
      expect(result.current.errors).toEqual({})
      expect(result.current.isLoading).toBe(false)
    })
  })

  describe('Verification Code Handling', () => {
    it('sanitizes verification code input', () => {
      const { result } = renderHook(() => useVerification(mockEmail), {
        wrapper: BrowserRouter,
      })

      act(() => {
        result.current.handleVerificationCodeChange('abc123')
      })

      expect(result.current.verificationCode).toBe('ABC123')
    })

    it('limits code to 6 characters', () => {
      const { result } = renderHook(() => useVerification(mockEmail), {
        wrapper: BrowserRouter,
      })

      act(() => {
        result.current.handleVerificationCodeChange('1234567890')
      })

      expect(result.current.verificationCode).toBe('123456')
    })
  })

  describe('Verification Submission', () => {
    it('submits verification successfully', async () => {
      authService.verifyRegistration.mockResolvedValue({})
      const { result } = renderHook(() => useVerification(mockEmail), {
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
      expect(authService.verifyRegistration).toHaveBeenCalledWith({
        email: mockEmail,
        verificationCode: 'ABC123',
      })
    })

    it('handles verification error', async () => {
      authService.verifyRegistration.mockRejectedValue(new Error('Invalid code'))
      const { result } = renderHook(() => useVerification(mockEmail), {
        wrapper: BrowserRouter,
      })

      await act(async () => {
        await result.current.handleSubmit()
      })

      expect(result.current.errors.submit).toBe('Invalid code')
    })
  })

  describe('Resend Code', () => {
    it('resends code successfully', async () => {
      authService.resendVerificationCode.mockResolvedValue({})
      const { result } = renderHook(() => useVerification(mockEmail), {
        wrapper: BrowserRouter,
      })

      await act(async () => {
        await result.current.handleResendCode()
      })

      expect(authService.resendVerificationCode).toHaveBeenCalledWith({ email: mockEmail })
      expect(result.current.resendMessage).toContain('resent successfully')
    })

    it('handles resend error', async () => {
      authService.resendVerificationCode.mockRejectedValue(new Error('Resend failed'))
      const { result } = renderHook(() => useVerification(mockEmail), {
        wrapper: BrowserRouter,
      })

      await act(async () => {
        await result.current.handleResendCode()
      })

      expect(result.current.errors.submit).toBe('Resend failed')
    })
  })

  describe('Reset', () => {
    it('resets verification state', () => {
      const { result } = renderHook(() => useVerification(mockEmail), {
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
