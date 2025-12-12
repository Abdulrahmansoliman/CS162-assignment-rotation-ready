import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import SignupPage from '@/features/auth/pages/signup'
import * as useSignupModule from '@/features/auth/hooks/useSignup'
import * as useVerificationModule from '@/features/auth/hooks/useVerification'

// Mock the hooks
vi.mock('@/features/auth/hooks/useSignup')
vi.mock('@/features/auth/hooks/useVerification')

describe('SignupPage', () => {
  const mockSignup = {
    formData: {
      firstName: '',
      lastName: '',
      email: '',
      cityId: '',
    },
    isLoading: false,
    errors: {},
    handleChange: vi.fn(),
    handleSubmit: vi.fn(),
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
    useSignupModule.useSignup = vi.fn(() => mockSignup)
    useVerificationModule.useVerification = vi.fn(() => mockVerification)
  })

  const renderSignupPage = () => {
    return render(
      <BrowserRouter>
        <SignupPage />
      </BrowserRouter>
    )
  }

  describe('Registration Form', () => {
    it('renders signup form with correct elements', () => {
      renderSignupPage()

      expect(screen.getByText("Let's start the journey!")).toBeInTheDocument()
      expect(screen.getByLabelText('First Name')).toBeInTheDocument()
      expect(screen.getByLabelText('Last Name')).toBeInTheDocument()
      expect(screen.getByLabelText('Email')).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /create account/i })).toBeInTheDocument()
    })

    it('handles first name input', () => {
      renderSignupPage()

      const firstNameInput = screen.getByLabelText('First Name')
      fireEvent.change(firstNameInput, { target: { value: 'John' } })

      expect(mockSignup.handleChange).toHaveBeenCalledWith('firstName', 'John')
    })

    it('handles last name input', () => {
      renderSignupPage()

      const lastNameInput = screen.getByLabelText('Last Name')
      fireEvent.change(lastNameInput, { target: { value: 'Doe' } })

      expect(mockSignup.handleChange).toHaveBeenCalledWith('lastName', 'Doe')
    })

    it('handles email input', () => {
      renderSignupPage()

      const emailInput = screen.getByLabelText('Email')
      fireEvent.change(emailInput, { target: { value: 'john@uni.minerva.edu' } })

      expect(mockSignup.handleChange).toHaveBeenCalledWith('email', 'john@uni.minerva.edu')
    })

    it('shows field validation errors', () => {
      useSignupModule.useSignup = vi.fn(() => ({
        ...mockSignup,
        errors: {
          firstName: 'First name is required',
          lastName: 'Last name is required',
          email: 'Invalid email format',
          cityId: 'Please select a city',
        },
      }))

      renderSignupPage()

      expect(screen.getByText('First name is required')).toBeInTheDocument()
      expect(screen.getByText('Last name is required')).toBeInTheDocument()
      expect(screen.getByText('Invalid email format')).toBeInTheDocument()
      expect(screen.getByText('Please select a city')).toBeInTheDocument()
    })

    it('shows submit error', () => {
      const errorMessage = 'Registration failed'
      useSignupModule.useSignup = vi.fn(() => ({
        ...mockSignup,
        errors: { submit: errorMessage },
      }))

      renderSignupPage()

      expect(screen.getByText(errorMessage)).toBeInTheDocument()
    })

    it('disables all inputs when loading', () => {
      useSignupModule.useSignup = vi.fn(() => ({
        ...mockSignup,
        isLoading: true,
      }))

      renderSignupPage()

      expect(screen.getByLabelText('First Name')).toBeDisabled()
      expect(screen.getByLabelText('Last Name')).toBeDisabled()
      expect(screen.getByLabelText('Email')).toBeDisabled()
      expect(screen.getByRole('button', { name: /create account/i })).toBeDisabled()
    })
  })
})
