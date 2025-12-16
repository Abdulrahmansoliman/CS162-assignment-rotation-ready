import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Routes, Route } from 'react-router-dom'
import HomePage from '@/features/home/HomePage'
import ItemDetailPage from '@/features/item/pages/item'
import * as homeService from '@/features/home/services/homeService'
import * as itemApi from '@/api/item'

vi.mock('@/features/home/services/homeService')
vi.mock('@/api/item')

describe('Integration: Item Navigation Access', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    homeService.fetchHomePageData.mockResolvedValue({
      userName: 'Test User',
      locale: { welcomeText: 'Welcome', color: '#007bff', cssClass: 'test' },
      categories: [],
      places: []
    })
  })

  it('can access home page', async () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <Routes>
          <Route path="/" element={<HomePage />} />
        </Routes>
      </MemoryRouter>
    )

    await waitFor(() => {
      expect(screen.getByText('All Places')).toBeInTheDocument()
    })
  })

  it('can access item detail page', async () => {
    itemApi.getItemById.mockResolvedValue({
      item_id: 1,
      name: 'Test Place',
      location: '123 Test St',
      walking_distance: 400,
      rotation_city: { name: 'San Francisco', time_zone: 'PST' },
      categories: [],
      tags: [],
      added_by_user: { first_name: 'John', last_name: 'Doe', email: 'john@test.com' }
    })

    render(
      <MemoryRouter initialEntries={['/item/1']}>
        <Routes>
          <Route path="/item/:id" element={<ItemDetailPage />} />
        </Routes>
      </MemoryRouter>
    )

    await waitFor(() => {
      expect(screen.getByText('Test Place')).toBeInTheDocument()
    })
  })
})
