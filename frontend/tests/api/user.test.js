import { describe, it, expect, vi, beforeEach } from 'vitest'
import { getCurrentUser, updateUserProfile } from '@/api/user'
import * as api from '@/api/index'

vi.mock('@/api/index')

describe('user API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('fetches current user successfully', async () => {
    const mockUser = {
      email: 'test@uni.minerva.edu',
      first_name: 'John',
      last_name: 'Doe',
      rotation_city: { city_id: 1, city_name: 'San Francisco' },
    }
    api.apiFetch.mockResolvedValue(mockUser)

    const result = await getCurrentUser()
    expect(result).toEqual(mockUser)
    expect(api.apiFetch).toHaveBeenCalledWith('/user/me', { method: 'GET' })
  })

  it('handles unauthorized user fetch', async () => {
    api.apiFetch.mockRejectedValue(new Error('401 Unauthorized'))

    await expect(getCurrentUser()).rejects.toThrow('401 Unauthorized')
  })

  it('updates user profile successfully', async () => {
    const updateData = { first_name: 'Jane', last_name: 'Smith' }
    api.apiFetch.mockResolvedValue({ success: true })

    const result = await updateUserProfile(updateData)
    expect(result).toEqual({ success: true })
    expect(api.apiFetch).toHaveBeenCalledWith('/user/me', {
      method: 'PUT',
      body: JSON.stringify(updateData)
    })
  })

  it('handles profile update errors', async () => {
    api.apiFetch.mockRejectedValue(new Error('400 Bad Request'))

    await expect(updateUserProfile({ first_name: '' })).rejects.toThrow('400 Bad Request')
  })

  it('handles forbidden profile update', async () => {
    api.apiFetch.mockRejectedValue(new Error('403 Forbidden'))

    await expect(updateUserProfile({ email: 'new@email.com' })).rejects.toThrow('403 Forbidden')
  })
})
