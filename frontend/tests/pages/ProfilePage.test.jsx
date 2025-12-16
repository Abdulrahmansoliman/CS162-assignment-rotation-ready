import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import ProfilePage from '@/features/profile/ProfilePage'
import * as userApi from '@/api/user'
import * as citiesApi from '@/api/cities'

vi.mock('@/api/user')
vi.mock('@/api/cities')

describe('ProfilePage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    userApi.getCurrentUser = vi.fn().mockResolvedValue({
      email: 'john@uni.minerva.edu',
      first_name: 'John',
      last_name: 'Doe',
      rotation_city: { city_id: 1, city_name: 'San Francisco' },
    })
    citiesApi.getCities = vi.fn().mockResolvedValue([
      { city_id: 1, city_name: 'San Francisco' },
    ])
    userApi.updateUserProfile = vi.fn().mockResolvedValue({})
  })

  it('renders profile page with user data', async () => {
    render(
      <BrowserRouter>
        <ProfilePage />
      </BrowserRouter>
    )

    await waitFor(() => {
      expect(screen.getByText('My Profile')).toBeInTheDocument()
      expect(screen.getByDisplayValue('john@uni.minerva.edu')).toBeInTheDocument()
    })
  })
})
