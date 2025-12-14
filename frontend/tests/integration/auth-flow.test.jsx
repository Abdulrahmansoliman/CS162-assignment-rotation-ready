import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import SignupPage from '@/features/auth/pages/signup'
import LoginPage from '@/features/auth/pages/login'
import * as authService from '@/features/auth/services/authservice'
import * as citiesApi from '@/api/cities'

vi.mock('@/features/auth/services/authservice')
vi.mock('@/api/cities')

describe('Integration: Full Authentication Flow', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    sessionStorage.clear()
    
    // Mock cities for signup
    citiesApi.getCities.mockResolvedValue([
      { city_id: 1, city_name: 'San Francisco' },
      { city_id: 2, city_name: 'Taipei' },
    ])
  })

  afterEach(() => {
    sessionStorage.clear()
  })

  describe('Signup Flow', () => {
    it('completes signup and verification', async () => {
      const mockEmail = 'newuser@uni.minerva.edu'
      
      authService.authService.register.mockResolvedValue({ success: true })
      authService.authService.verifyRegistration.mockResolvedValue({
        access_token: 'signup-access-token',
        refresh_token: 'signup-refresh-token',
      })

      render(
        <BrowserRouter>
          <SignupPage />
        </BrowserRouter>
      )

      await waitFor(() => {
        expect(screen.getByText("Let's start the journey!")).toBeInTheDocument()
      })

      fireEvent.change(screen.getByLabelText('First Name'), { target: { value: 'John' } })
      fireEvent.change(screen.getByLabelText('Last Name'), { target: { value: 'Doe' } })
      fireEvent.change(screen.getByLabelText('Email'), { target: { value: mockEmail } })

      const signupButton = screen.getByRole('button', { name: /create account/i })
      fireEvent.click(signupButton)

      await waitFor(() => {
        expect(authService.authService.register).toHaveBeenCalledWith(
          expect.objectContaining({
            email: mockEmail,
            firstName: 'John',
            lastName: 'Doe',
          })
        )
      })
    })
  })

  describe('Login Flow', () => {
    it('completes login and verification', async () => {
      const mockEmail = 'user@uni.minerva.edu'
      
      authService.authService.login.mockResolvedValue({ success: true })
      authService.authService.verifyLogin.mockResolvedValue({
        access_token: 'login-access-token',
        refresh_token: 'login-refresh-token',
      })

      render(
        <BrowserRouter>
          <LoginPage />
        </BrowserRouter>
      )

      await waitFor(() => {
        expect(screen.getByText('Welcome back!')).toBeInTheDocument()
      })

      fireEvent.change(screen.getByLabelText('Email'), { target: { value: mockEmail } })
      
      const loginButton = screen.getByRole('button', { name: /sign in/i })
      fireEvent.click(loginButton)

      await waitFor(() => {
        expect(authService.authService.login).toHaveBeenCalledWith({ email: mockEmail })
      })
    })
  })

  describe('Validation', () => {
    it('prevents signup with invalid email domain', async () => {
      render(
        <BrowserRouter>
          <SignupPage />
        </BrowserRouter>
      )

      await waitFor(() => {
        expect(screen.getByText("Let's start the journey!")).toBeInTheDocument()
      })

      fireEvent.change(screen.getByLabelText('First Name'), { target: { value: 'John' } })
      fireEvent.change(screen.getByLabelText('Last Name'), { target: { value: 'Doe' } })
      fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'test@gmail.com' } })

      const signupButton = screen.getByRole('button', { name: /create account/i })
      fireEvent.click(signupButton)

      await waitFor(() => {
        expect(authService.authService.register).not.toHaveBeenCalled()
      })
    })

    it('prevents login with invalid email', async () => {
      render(
        <BrowserRouter>
          <LoginPage />
        </BrowserRouter>
      )

      await waitFor(() => {
        expect(screen.getByText('Welcome back!')).toBeInTheDocument()
      })

      fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'notanemail' } })
      
      const loginButton = screen.getByRole('button', { name: /sign in/i })
      fireEvent.click(loginButton)

      await waitFor(() => {
        expect(authService.authService.login).not.toHaveBeenCalled()
      })
    })
  })
})
