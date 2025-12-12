import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, act, waitFor } from '@testing-library/react'
import { useLogin } from '@/features/auth/hooks/useLogin'
import { authService } from '@/features/auth/services/authservice'

vi.mock('@/features/auth/services/authservice')

describe('useLogin', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('Initial State', () => {
    it('initializes with empty email and no errors', () => {
      const { result } = renderHook(() => useLogin())

      expect(result.current.email).toBe('')
      expect(result.current.errors).toEqual({})
      expect(result.current.isLoading).toBe(false)
    })
  })

  describe('Email Handling', () => {
    it('updates email on change', () => {
      const { result } = renderHook(() => useLogin())

      act(() => {
        result.current.handleChange('test@uni.minerva.edu')
      })

      expect(result.current.email).toBe('test@uni.minerva.edu')
    })

    it('clears email error on change', () => {
      const { result } = renderHook(() => useLogin())

      act(() => {
        result.current.handleSubmit()
      })

      expect(result.current.errors.email).toBeTruthy()

      act(() => {
        result.current.handleChange('test@uni.minerva.edu')
      })

      expect(result.current.errors.email).toBeNull()
    })
  })

  describe('Form Submission', () => {
    it('validates email before submission', async () => {
      const { result } = renderHook(() => useLogin())

      let submitResult
      await act(async () => {
        submitResult = await result.current.handleSubmit()
      })

      expect(submitResult.success).toBe(false)
      expect(result.current.errors.email).toBeTruthy()
      expect(authService.login).not.toHaveBeenCalled()
    })

    it('submits valid email successfully', async () => {
      authService.login.mockResolvedValue({})
      const { result } = renderHook(() => useLogin())

      act(() => {
        result.current.handleChange('test@uni.minerva.edu')
      })

      let submitResult
      await act(async () => {
        submitResult = await result.current.handleSubmit()
      })

      expect(submitResult.success).toBe(true)
      expect(authService.login).toHaveBeenCalledWith({ email: 'test@uni.minerva.edu' })
    })

    it('handles submission error', async () => {
      authService.login.mockRejectedValue(new Error('Login failed'))
      const { result } = renderHook(() => useLogin())

      act(() => {
        result.current.handleChange('test@uni.minerva.edu')
      })

      let submitResult
      await act(async () => {
        submitResult = await result.current.handleSubmit()
      })

      expect(submitResult.success).toBe(false)
      expect(result.current.errors.submit).toBe('Login failed')
    })

    it('sets loading state during submission', async () => {
      authService.login.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)))
      const { result } = renderHook(() => useLogin())

      act(() => {
        result.current.handleChange('test@uni.minerva.edu')
      })

      let submitPromise
      act(() => {
        submitPromise = result.current.handleSubmit()
      })

      expect(result.current.isLoading).toBe(true)

      await act(async () => {
        await submitPromise
      })

      expect(result.current.isLoading).toBe(false)
    })
  })
})
