import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import SignupPage from '@/features/auth/pages/signup'
import LoginPage from '@/features/auth/pages/login'
import * as citiesApi from '@/api/cities'

vi.mock('@/api/cities')

describe('Integration: Authentication Access', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    citiesApi.getCities.mockResolvedValue([
      { city_id: 1, city_name: 'San Francisco' },
    ])
  })

  it('can access signup page', async () => {
    render(
      <BrowserRouter>
        <SignupPage />
      </BrowserRouter>
    )

    await waitFor(() => {
      expect(screen.getByLabelText(/first name/i)).toBeInTheDocument()
    })
  })

  it('can access login page', async () => {
    render(
      <BrowserRouter>
        <LoginPage />
      </BrowserRouter>
    )

    await waitFor(() => {
      expect(screen.getByPlaceholderText(/example.com/i)).toBeInTheDocument()
    })
  })
})
