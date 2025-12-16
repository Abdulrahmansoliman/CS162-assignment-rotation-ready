import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook } from '@testing-library/react'
import { useLogin } from '@/features/auth/hooks/useLogin'

vi.mock('@/features/auth/services/authservice')

describe('useLogin', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('hook initializes successfully', () => {
    const { result } = renderHook(() => useLogin())
    expect(result.current.email).toBe('')
    expect(result.current.errors).toEqual({})
  })
})
