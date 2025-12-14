import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes, Navigate } from 'react-router-dom'
import ProfilePage from '@/features/profile/ProfilePage'
import LoginPage from '@/features/auth/pages/login'
import * as authService from '@/features/auth/services/authservice'
import * as apiIndex from '@/api/index'
import * as userApi from '@/api/user'
import * as citiesApi from '@/api/cities'

vi.mock('@/features/auth/services/authservice')
vi.mock('@/api/user')
vi.mock('@/api/cities')
vi.mock('@/api/index', async () => {
  const actual = await vi.importActual('@/api/index')
  return {
    ...actual,
    apiFetch: vi.fn(),
    checkAuth: vi.fn(),
  }
})

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
    sessionStorage.clear()
    
    // Default mocks
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

  afterEach(() => {
    sessionStorage.clear()
  })

  describe('Unauthenticated Access', () => {
    it('redirects to login when accessing protected route without token', async () => {
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
        expect(screen.getByText('Welcome back!')).toBeInTheDocument()
      })

      // Profile page should not render
      expect(screen.queryByText('My Profile')).not.toBeInTheDocument()
    })

    it('blocks protected route without authentication', async () => {
      authService.getAccessToken.mockReturnValue(null)

      const ProtectedPage = () => <div>Protected Content</div>

      render(
        <MemoryRouter initialEntries={['/protected']}>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route
              path="/protected"
              element={
                <ProtectedRoute>
                  <ProtectedPage />
                </ProtectedRoute>
              }
            />
          </Routes>
        </MemoryRouter>
      )

      await waitFor(() => {
        expect(screen.getByText('Welcome back!')).toBeInTheDocument()
      })

      expect(screen.queryByText('Protected Content')).not.toBeInTheDocument()
    })
  })

  describe('Authenticated Access', () => {
    it('allows access to protected route with valid token', async () => {
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

      // Should render profile page
      await waitFor(() => {
        expect(screen.getByText('My Profile')).toBeInTheDocument()
      })

      // Login page should not render
      expect(screen.queryByText('Welcome back!')).not.toBeInTheDocument()
    })

    it('maintains access to protected route with valid token', async () => {
      authService.getAccessToken.mockReturnValue('valid-token')

      const ProtectedPage = () => <div>Protected Content</div>

      render(
        <MemoryRouter initialEntries={['/protected']}>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route
              path="/protected"
              element={
                <ProtectedRoute>
                  <ProtectedPage />
                </ProtectedRoute>
              }
            />
          </Routes>
        </MemoryRouter>
      )

      await waitFor(() => {
        expect(screen.getByText('Protected Content')).toBeInTheDocument()
      })

      expect(screen.queryByText('Welcome back!')).not.toBeInTheDocument()
    })
  })

  describe('Token Expiration', () => {
    it('blocks access when no token exists', async () => {
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

      await waitFor(() => {
        expect(screen.getByText('Welcome back!')).toBeInTheDocument()
      })

      expect(screen.queryByText('My Profile')).not.toBeInTheDocument()
    })
  })
})
