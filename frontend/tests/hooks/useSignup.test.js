import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook } from '@testing-library/react'
import { useSignup, validateEmail } from '@/features/auth/hooks/useSignup'
import { authService } from '@/features/auth/services/authservice'

vi.mock('@/features/auth/services/authservice')

describe('useSignup', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('hook initializes successfully', () => {
    const { result } = renderHook(() => useSignup())
    expect(result.current.formData).toBeDefined()
    expect(result.current.handleChange).toBeDefined()
  })

  it('validates email correctly', () => {
    expect(validateEmail('test@uni.minerva.edu')).toBeNull()
    expect(validateEmail('test@minerva.edu')).toBeNull()
    expect(validateEmail('test@gmail.com')).toContain('minerva.edu')
  })
})
