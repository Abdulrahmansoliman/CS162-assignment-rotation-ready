import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import SignupPage from '@/features/auth/pages/signup'
import * as useSignupModule from '@/features/auth/hooks/useSignup'
import * as useVerificationModule from '@/features/auth/hooks/useVerification'

vi.mock('@/features/auth/hooks/useSignup')
vi.mock('@/features/auth/hooks/useVerification')

describe('SignupPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    useSignupModule.useSignup = vi.fn(() => ({
      formData: { firstName: '', lastName: '', email: '', cityId: '' },
      isLoading: false,
      errors: {},
      handleChange: vi.fn(),
      handleSubmit: vi.fn(),
    }))
    useVerificationModule.useVerification = vi.fn(() => ({
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

  it('can access signup page', async () => {
    render(
      <BrowserRouter>
        <SignupPage />
      </BrowserRouter>
    )

    // Just verify the signup form fields render
    await waitFor(() => {
      expect(screen.getByLabelText(/first name/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/last name/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    })
  })
})
