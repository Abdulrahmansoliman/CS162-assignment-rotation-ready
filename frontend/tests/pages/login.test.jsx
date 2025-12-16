import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import LoginPage from '@/features/auth/pages/login'
import * as useLoginModule from '@/features/auth/hooks/useLogin'
import * as useLoginVerificationModule from '@/features/auth/hooks/useLoginVerification'

vi.mock('@/features/auth/hooks/useLogin')
vi.mock('@/features/auth/hooks/useLoginVerification')

describe('LoginPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    useLoginModule.useLogin = vi.fn(() => ({
      email: '',
      isLoading: false,
      errors: {},
      handleChange: vi.fn(),
      handleSubmit: vi.fn().mockResolvedValue({ success: false }),
    }))
    useLoginVerificationModule.useLoginVerification = vi.fn(() => ({
      verificationCode: '',
      isLoading: false,
      isResending: false,
      errors: {},
      resendMessage: '',
      handleVerificationCodeChange: vi.fn(),
      handleSubmit: vi.fn(),
      handleResendCode: vi.fn(),
      reset: vi.fn(),
    }))
  })

  it('can access login page', () => {
    render(
      <BrowserRouter>
        <LoginPage />
      </BrowserRouter>
    )

    // Just verify the page renders with an email input field
    expect(screen.getByPlaceholderText(/example.com/i)).toBeInTheDocument()
  })
})
