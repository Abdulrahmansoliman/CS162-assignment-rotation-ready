import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes, Navigate } from 'react-router-dom'
import ProfilePage from '@/features/profile/ProfilePage'
import LoginPage from '@/features/auth/pages/login'
import * as authService from '@/features/auth/services/authservice'
import * as userApi from '@/api/user'
import * as citiesApi from '@/api/cities'

vi.mock('@/features/auth/services/authservice')
vi.mock('@/api/user')
vi.mock('@/api/cities')

function ProtectedRoute({ children }) {
  const token = authService.getAccessToken()
  if (!token) {
    return <Navigate to="/login" replace />
  }
  return children
}

describe('Integration: Protected Route Access', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    citiesApi.getCities.mockResolvedValue([
      { city_id: 1, city_name: 'San Francisco' },
    ])
    userApi.getCurrentUser.mockResolvedValue({
      email: 'test@uni.minerva.edu',
      first_name: 'John',
      last_name: 'Doe',
      rotation_city: { city_id: 1, city_name: 'San Francisco' },
    })
  })

  it('blocks access without token', async () => {
    authService.getAccessToken.mockReturnValue(null)

    render(
      <MemoryRouter initialEntries={['/profile']}>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <ProfilePage />
              </ProtectedRoute>
            }
          />
        </Routes>
      </MemoryRouter>
    )

    // Should be redirected to login page
    await waitFor(() => {
      expect(screen.getByPlaceholderText(/example.com/i)).toBeInTheDocument()
    })
  })

  it('allows access with valid token', async () => {
    authService.getAccessToken.mockReturnValue('valid-token')

    render(
      <MemoryRouter initialEntries={['/profile']}>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <ProfilePage />
              </ProtectedRoute>
            }
          />
        </Routes>
      </MemoryRouter>
    )

    await waitFor(() => {
      expect(screen.getByText('My Profile')).toBeInTheDocument()
    })
  })
})
