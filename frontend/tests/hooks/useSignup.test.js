import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { useSignup, validateEmail } from '@/features/auth/hooks/useSignup'
import { authService } from '@/features/auth/services/authservice'

vi.mock('@/features/auth/services/authservice')

describe('validateEmail', () => {
  it('accepts valid uni.minerva.edu email', () => {
    expect(validateEmail('test@uni.minerva.edu')).toBeNull()
  })

  it('accepts valid minerva.edu email', () => {
    expect(validateEmail('test@minerva.edu')).toBeNull()
  })

  it('rejects non-Minerva email', () => {
    const error = validateEmail('test@gmail.com')
    expect(error).toContain('minerva.edu')
  })

  it('rejects invalid email format', () => {
    const error = validateEmail('notanemail')
    expect(error).toContain('minerva.edu')
  })
})

describe('useSignup', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('Initial State', () => {
    it('initializes with empty form data', () => {
      const { result } = renderHook(() => useSignup())

      expect(result.current.formData).toEqual({
        firstName: '',
        lastName: '',
        email: '',
        cityId: '',
      })
      expect(result.current.errors).toEqual({})
      expect(result.current.isLoading).toBe(false)
    })
  })

  describe('Form Field Updates', () => {
    it('updates firstName field', () => {
      const { result } = renderHook(() => useSignup())

      act(() => {
        result.current.handleChange('firstName', 'John')
      })

      expect(result.current.formData.firstName).toBe('John')
    })

    it('updates lastName field', () => {
      const { result } = renderHook(() => useSignup())

      act(() => {
        result.current.handleChange('lastName', 'Doe')
      })

      expect(result.current.formData.lastName).toBe('Doe')
    })

    it('updates email field', () => {
      const { result } = renderHook(() => useSignup())

      act(() => {
        result.current.handleChange('email', 'john@uni.minerva.edu')
      })

      expect(result.current.formData.email).toBe('john@uni.minerva.edu')
    })

    it('updates cityId field', () => {
      const { result } = renderHook(() => useSignup())

      act(() => {
        result.current.handleChange('cityId', '1')
      })

      expect(result.current.formData.cityId).toBe('1')
    })

    it('clears field error on change', () => {
      const { result } = renderHook(() => useSignup())

      act(() => {
        result.current.handleSubmit()
      })

      expect(result.current.errors.email).toBeTruthy()

      act(() => {
        result.current.handleChange('email', 'test@uni.minerva.edu')
      })

      expect(result.current.errors.email).toBeNull()
    })
  })

  describe('Form Submission', () => {
    it('validates email before submission', async () => {
      const { result } = renderHook(() => useSignup())

      act(() => {
        result.current.handleChange('firstName', 'John')
        result.current.handleChange('lastName', 'Doe')
        result.current.handleChange('email', 'invalid@gmail.com')
        result.current.handleChange('cityId', '1')
      })

      let submitResult
      await act(async () => {
        submitResult = await result.current.handleSubmit()
      })

      expect(submitResult.success).toBe(false)
      expect(result.current.errors.email).toBeTruthy()
      expect(authService.register).not.toHaveBeenCalled()
    })

    it('submits valid form successfully', async () => {
      authService.register.mockResolvedValue({})
      const { result } = renderHook(() => useSignup())

      act(() => {
        result.current.handleChange('firstName', 'John')
        result.current.handleChange('lastName', 'Doe')
        result.current.handleChange('email', 'john@uni.minerva.edu')
        result.current.handleChange('cityId', '1')
      })

      let submitResult
      await act(async () => {
        submitResult = await result.current.handleSubmit()
      })

      expect(submitResult.success).toBe(true)
      expect(authService.register).toHaveBeenCalledWith({
        email: 'john@uni.minerva.edu',
        cityId: '1',
        firstName: 'John',
        lastName: 'Doe',
      })
    })

    it('handles submission error', async () => {
      authService.register.mockRejectedValue(new Error('Registration failed'))
      const { result } = renderHook(() => useSignup())

      act(() => {
        result.current.handleChange('firstName', 'John')
        result.current.handleChange('lastName', 'Doe')
        result.current.handleChange('email', 'john@uni.minerva.edu')
        result.current.handleChange('cityId', '1')
      })

      let submitResult
      await act(async () => {
        submitResult = await result.current.handleSubmit()
      })

      expect(submitResult.success).toBe(false)
      expect(result.current.errors.submit).toBe('Registration failed')
    })
  })
})
