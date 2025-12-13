import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import LoginPage from '@/features/auth/pages/login'
import * as useLoginModule from '@/features/auth/hooks/useLogin'
import * as useLoginVerificationModule from '@/features/auth/hooks/useLoginVerification'

// Mock the hooks
vi.mock('@/features/auth/hooks/useLogin')
vi.mock('@/features/auth/hooks/useLoginVerification')

describe('LoginPage', () => {
  const mockLogin = {
    email: '',
    isLoading: false,
    errors: {},
    handleChange: vi.fn(),
    handleSubmit: vi.fn().mockResolvedValue({ success: false }),
  }

  const mockVerification = {
    verificationCode: '',
    isLoading: false,
    isResending: false,
    errors: {},
    resendMessage: '',
    handleVerificationCodeChange: vi.fn(),
    handleSubmit: vi.fn(),
    handleResendCode: vi.fn(),
    reset: vi.fn(),
  }

  beforeEach(() => {
    vi.clearAllMocks()
    useLoginModule.useLogin = vi.fn(() => mockLogin)
    useLoginVerificationModule.useLoginVerification = vi.fn(() => mockVerification)
  })

  const renderLoginPage = () => {
    return render(
      <BrowserRouter>
        <LoginPage />
      </BrowserRouter>
    )
  }

  describe('Login Form', () => {
    it('renders login form with correct elements', () => {
      renderLoginPage()

      expect(screen.getByText('Welcome back!')).toBeInTheDocument()
      expect(screen.getByText('Enter your email to sign in')).toBeInTheDocument()
      expect(screen.getByLabelText('Email')).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument()
    })

    it('displays email input with correct attributes', () => {
      renderLoginPage()

      const emailInput = screen.getByLabelText('Email')
      expect(emailInput).toHaveAttribute('type', 'email')
      expect(emailInput).toHaveAttribute('placeholder', 'john@uni.minerva.edu')
      expect(emailInput).toBeRequired()
    })

    it('handles email input change', () => {
      renderLoginPage()

      const emailInput = screen.getByLabelText('Email')
      fireEvent.change(emailInput, { target: { value: 'test@uni.minerva.edu' } })

      expect(mockLogin.handleChange).toHaveBeenCalledWith('test@uni.minerva.edu')
    })

    it('shows email validation error', () => {
      const errorMessage = 'Invalid email format'
      useLoginModule.useLogin = vi.fn(() => ({
        ...mockLogin,
        errors: { email: errorMessage },
      }))

      renderLoginPage()

      expect(screen.getByText(errorMessage)).toBeInTheDocument()
    })

    it('shows submit error', () => {
      const errorMessage = 'Login failed'
      useLoginModule.useLogin = vi.fn(() => ({
        ...mockLogin,
        errors: { submit: errorMessage },
      }))

      renderLoginPage()

      expect(screen.getByText(errorMessage)).toBeInTheDocument()
    })

    it('disables input and button when loading', () => {
      useLoginModule.useLogin = vi.fn(() => ({
        ...mockLogin,
        isLoading: true,
      }))

      renderLoginPage()

      const emailInput = screen.getByLabelText('Email')
      const submitButton = screen.getByRole('button', { name: /sign in/i })

      expect(emailInput).toBeDisabled()
      expect(submitButton).toBeDisabled()
    })
  })
})
