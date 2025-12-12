import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import ProfilePage from '../ProfilePage'
import * as userApi from '@/api/user'
import * as citiesApi from '@/api/cities'

// Mock the API modules
vi.mock('@/api/user')
vi.mock('@/api/cities')

describe('ProfilePage', () => {
  const mockUser = {
    email: 'john@uni.minerva.edu',
    first_name: 'John',
    last_name: 'Doe',
    rotation_city: {
      city_id: 1,
      city_name: 'San Francisco',
    },
  }

  const mockCities = [
    { city_id: 1, city_name: 'San Francisco' },
    { city_id: 2, city_name: 'Taipei' },
    { city_id: 3, city_name: 'Seoul' },
    { city_id: 4, city_name: 'Buenos Aires' },
    { city_id: 5, city_name: 'India' },
    { city_id: 6, city_name: 'Berlin' },
  ]

  beforeEach(() => {
    vi.clearAllMocks()
    userApi.getCurrentUser = vi.fn().mockResolvedValue(mockUser)
    citiesApi.getCities = vi.fn().mockResolvedValue(mockCities)
    userApi.updateUserProfile = vi.fn().mockResolvedValue({})
  })

  describe('Loading State', () => {
    it('loads user data and cities on mount', async () => {
      render(<ProfilePage />)

      await waitFor(() => {
        expect(userApi.getCurrentUser).toHaveBeenCalledTimes(1)
        expect(citiesApi.getCities).toHaveBeenCalledTimes(1)
      })
    })
  })

  describe('Profile Display', () => {
    it('renders profile page with correct title', async () => {
      render(<ProfilePage />)

      await waitFor(() => {
        expect(screen.getByText('My Profile')).toBeInTheDocument()
        expect(screen.getByText('Update your personal information and rotation city.')).toBeInTheDocument()
      })
    })

    it('displays user email as disabled field', async () => {
      render(<ProfilePage />)

      await waitFor(() => {
        const emailInput = screen.getByDisplayValue('john@uni.minerva.edu')
        expect(emailInput).toBeInTheDocument()
        expect(emailInput).toBeDisabled()
        expect(emailInput).toHaveAttribute('type', 'email')
      })
    })

    it('displays first name in editable field', async () => {
      render(<ProfilePage />)

      await waitFor(() => {
        const firstNameInput = screen.getByDisplayValue('John')
        expect(firstNameInput).toBeInTheDocument()
        expect(firstNameInput).not.toBeDisabled()
      })
    })

    it('displays last name in editable field', async () => {
      render(<ProfilePage />)

      await waitFor(() => {
        const lastNameInput = screen.getByDisplayValue('Doe')
        expect(lastNameInput).toBeInTheDocument()
        expect(lastNameInput).not.toBeDisabled()
      })
    })
  })

  describe('Form Interactions', () => {
    it('updates first name on input change', async () => {
      render(<ProfilePage />)

      await waitFor(() => {
        const firstNameInput = screen.getByDisplayValue('John')
        fireEvent.change(firstNameInput, { target: { value: 'Jane' } })

        expect(firstNameInput).toHaveValue('Jane')
      })
    })

    it('updates last name on input change', async () => {
      render(<ProfilePage />)

      await waitFor(() => {
        const lastNameInput = screen.getByDisplayValue('Doe')
        fireEvent.change(lastNameInput, { target: { value: 'Smith' } })

        expect(lastNameInput).toHaveValue('Smith')
      })
    })
  })

  describe('Form Submission', () => {
    it('submits updated profile data', async () => {
      render(<ProfilePage />)

      await waitFor(() => {
        const firstNameInput = screen.getByDisplayValue('John')
        fireEvent.change(firstNameInput, { target: { value: 'Jane' } })

        const lastNameInput = screen.getByDisplayValue('Doe')
        fireEvent.change(lastNameInput, { target: { value: 'Smith' } })
      })

      const updateButton = screen.getByRole('button', { name: /save changes/i })
      fireEvent.click(updateButton)

      await waitFor(() => {
        expect(userApi.updateUserProfile).toHaveBeenCalledWith({
          first_name: 'Jane',
          last_name: 'Smith',
          rotation_city_id: 1,
        })
      })
    })

    it('shows success message after successful update', async () => {
      render(<ProfilePage />)

      await waitFor(() => {
        const updateButton = screen.getByRole('button', { name: /save changes/i })
        fireEvent.click(updateButton)
      })

      await waitFor(() => {
        expect(screen.getByText('Profile updated successfully!')).toBeInTheDocument()
      })
    })
  })

  describe('Error Handling', () => {
    it('shows error message when profile update fails', async () => {
      userApi.updateUserProfile = vi.fn().mockRejectedValue(new Error('Update failed'))

      render(<ProfilePage />)

      await waitFor(() => {
        const updateButton = screen.getByRole('button', { name: /save changes/i })
        fireEvent.click(updateButton)
      })

      await waitFor(() => {
        expect(screen.getByText('Failed to update profile')).toBeInTheDocument()
      })
    })
  })
})
