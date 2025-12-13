import { describe, it, expect, vi, beforeEach } from 'vitest'
import { getCities } from '@/api/cities'
import * as api from '@/api/index'

vi.mock('@/api/index')

describe('cities API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('getCities', () => {
    it('fetches cities with GET method', async () => {
      const mockCities = [
        { city_id: 1, city_name: 'San Francisco' },
        { city_id: 2, city_name: 'Taipei' },
        { city_id: 3, city_name: 'Seoul' },
      ]

      api.apiFetch.mockResolvedValue(mockCities)

      const result = await getCities()

      expect(api.apiFetch).toHaveBeenCalledWith('rotation-city', {
        method: 'GET',
      })
      expect(result).toEqual(mockCities)
    })

    it('handles fetch error', async () => {
      api.apiFetch.mockRejectedValue(new Error('Failed to fetch cities'))

      await expect(getCities()).rejects.toThrow('Failed to fetch cities')
    })
  })
})
