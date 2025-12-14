import { describe, it, expect, vi, beforeEach } from 'vitest'
import { getCurrentUser, updateUserProfile } from '@/api/user'
import * as api from '@/api/index'

vi.mock('@/api/index')

describe('user API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('getCurrentUser', () => {
    it('fetches current user with GET method', async () => {
      const mockUser = {
        email: 'test@uni.minerva.edu',
        first_name: 'John',
        last_name: 'Doe',
        rotation_city: {
          city_id: 1,
          city_name: 'San Francisco',
        },
      }

      api.apiFetch.mockResolvedValue(mockUser)

      const result = await getCurrentUser()

      expect(api.apiFetch).toHaveBeenCalledWith('user/me', {
        method: 'GET',
      })
      expect(result).toEqual(mockUser)
    })

    it('handles fetch error', async () => {
      api.apiFetch.mockRejectedValue(new Error('Unauthorized'))

      await expect(getCurrentUser()).rejects.toThrow('Unauthorized')
    })
  })

  describe('updateUserProfile', () => {
    it('updates user profile with PUT method', async () => {
      const updateData = {
        first_name: 'Jane',
        last_name: 'Smith',
        rotation_city_id: 2,
      }

      api.apiFetch.mockResolvedValue({ success: true })

      const result = await updateUserProfile(updateData)

      expect(api.apiFetch).toHaveBeenCalledWith('user/me', {
        method: 'PUT',
        body: JSON.stringify(updateData),
      })
      expect(result).toEqual({ success: true })
    })

    it('handles update error', async () => {
      api.apiFetch.mockRejectedValue(new Error('Update failed'))

      await expect(updateUserProfile({})).rejects.toThrow('Update failed')
    })
  })
})
