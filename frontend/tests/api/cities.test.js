import { describe, it, expect, vi, beforeEach } from 'vitest'
import { getCities } from '@/api/cities'
import * as api from '@/api/index'

vi.mock('@/api/index')

describe('cities API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('fetches cities successfully', async () => {
    const mockCities = [
      { city_id: 1, city_name: 'San Francisco' },
      { city_id: 2, city_name: 'Taipei' },
    ]
    api.apiFetch.mockResolvedValue(mockCities)

    const result = await getCities()
    expect(result).toEqual(mockCities)
  })
})
