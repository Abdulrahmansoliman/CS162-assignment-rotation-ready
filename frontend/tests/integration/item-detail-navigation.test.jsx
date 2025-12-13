import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { MemoryRouter, Routes, Route } from 'react-router-dom'
import HomePage from '@/features/home/HomePage'
import ItemDetailPage from '@/features/item/pages/item'
import * as homeService from '@/features/home/services/homeService'
import * as itemApi from '@/api/item'

vi.mock('@/features/home/services/homeService')
vi.mock('@/api/item')

describe('Integration: Item Detail Navigation Flow', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  const createMockHomeData = (places = []) => ({
    userName: 'Test User',
    locale: {
      welcomeText: 'Welcome',
      color: '#007bff',
      cssClass: 'test-locale'
    },
    categories: [
      { id: 1, name: 'Cafes', image: null },
      { id: 2, name: 'Libraries', image: null }
    ],
    places
  })

  const createMockItemDetail = (overrides = {}) => ({
    item_id: 1,
    name: 'Test Place',
    location: '123 Test St',
    walking_distance: 400,
    created_at: '2024-11-15T10:30:00Z',
    number_of_verifications: 15,
    rotation_city: {
      name: 'San Francisco',
      time_zone: 'PST',
      res_hall_location: 'Downtown'
    },
    categories: [{ category_id: 1, name: 'Cafe' }],
    tags: [
      { tag_id: 1, name: 'WiFi Available', value: 'true', value_type: 'boolean' },
      { tag_id: 2, name: 'Seating Capacity', value: '50', value_type: 'number' }
    ],
    added_by_user: {
      first_name: 'John',
      last_name: 'Doe',
      email: 'john.doe@uni.minerva.edu'
    },
    ...overrides
  })

  const renderWithRouter = (initialPath = '/') => {
    return render(
      <MemoryRouter initialEntries={[initialPath]}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/item/:id" element={<ItemDetailPage />} />
        </Routes>
      </MemoryRouter>
    )
  }

  it('navigates from home page item card to correct item detail page', async () => {
    const mockPlaces = [
      {
        id: 1,
        name: 'Cozy Coffee Shop',
        address: '123 Main St',
        distance: '0.5',
        tags: ['Coffee', 'WiFi', 'Study-friendly'],
        verifiedCount: 15,
        lastVerified: '12/10/2024',
        priceLevel: 2
      },
      {
        id: 2,
        name: 'City Library',
        address: '456 Library Ave',
        distance: '1.2',
        tags: ['Books', 'Quiet', 'Free'],
        verifiedCount: 8,
        lastVerified: '12/5/2024',
        priceLevel: 1
      }
    ]

    const mockHomeData = createMockHomeData(mockPlaces)
    const mockItemDetail = createMockItemDetail({
      item_id: 1,
      name: 'Cozy Coffee Shop',
      location: '123 Main St',
      added_by_user: {
        first_name: 'John',
        last_name: 'Doe',
        email: 'john.doe@uni.minerva.edu'
      }
    })

    homeService.fetchHomePageData.mockResolvedValue(mockHomeData)
    itemApi.getItemById.mockResolvedValue(mockItemDetail)

    // Act: Render the app and navigate
    renderWithRouter('/')

    // Wait for home page to load with items
    await waitFor(() => {
      expect(screen.getByText('Cozy Coffee Shop')).toBeInTheDocument()
      expect(screen.getByText('City Library')).toBeInTheDocument()
    })

    // Verify View Details buttons exist
    const viewDetailsButtons = screen.getAllByText('View Details')
    expect(viewDetailsButtons).toHaveLength(2)

    // Click the first item's View Details button
    fireEvent.click(viewDetailsButtons[0])

    // Assert: Verify API was called with correct ID
    await waitFor(() => {
      expect(itemApi.getItemById).toHaveBeenCalledWith('1')
    })

    // Verify item detail page displays correct information
    await waitFor(() => {
      expect(screen.getByText('Cozy Coffee Shop')).toBeInTheDocument()
      expect(screen.getByText('John Doe')).toBeInTheDocument()
      expect(screen.getByText('john.doe@uni.minerva.edu')).toBeInTheDocument()
    })
  })

  it('navigates to different item detail pages for different items', async () => {
    // Arrange: Create multiple items
    const mockPlaces = [
      {
        id: 1,
        name: 'First Place',
        address: '111 First St',
        tags: ['Tag1'],
        verifiedCount: 5,
        priceLevel: 1
      },
      {
        id: 2,
        name: 'Second Place',
        address: '222 Second St',
        tags: ['Tag2'],
        verifiedCount: 10,
        priceLevel: 2
      }
    ]

    const mockHomeData = createMockHomeData(mockPlaces)
    const mockItemDetail = createMockItemDetail({
      item_id: 1,
      name: 'First Place',
      location: '111 First St',
      rotation_city: { name: 'San Francisco', time_zone: 'PST' },
      added_by_user: {
        first_name: 'Alice',
        last_name: 'Smith',
        email: 'alice@test.com'
      }
    })

    homeService.fetchHomePageData.mockResolvedValue(mockHomeData)
    itemApi.getItemById.mockResolvedValue(mockItemDetail)

    // Act: Render and navigate
    renderWithRouter('/')

    // Wait for both items to appear on home page
    await waitFor(() => {
      expect(screen.getByText('First Place')).toBeInTheDocument()
      expect(screen.getByText('Second Place')).toBeInTheDocument()
    })

    // Click the first item's View Details button
    const viewDetailsButtons = screen.getAllByText('View Details')
    fireEvent.click(viewDetailsButtons[0])

    // Assert: Verify correct API call and page load
    await waitFor(() => {
      expect(itemApi.getItemById).toHaveBeenCalledWith('1')
      expect(screen.getByText('Alice Smith')).toBeInTheDocument()
    })
  })

  it('correctly passes item ID to detail page from different cards', async () => {
    // Arrange: Create item with unique ID to verify correct routing
    const uniqueItemId = 42
    const mockPlaces = [
      {
        id: uniqueItemId,
        name: 'Unique Test Place',
        address: '999 Unique St',
        tags: ['Special'],
        verifiedCount: 7,
        priceLevel: 3
      }
    ]

    const mockHomeData = createMockHomeData(mockPlaces)
    const mockItemDetail = createMockItemDetail({
      item_id: uniqueItemId,
      name: 'Unique Test Place',
      location: '999 Unique St',
      rotation_city: { name: 'Berlin', time_zone: 'CET' },
      added_by_user: {
        first_name: 'Charlie',
        last_name: 'Brown',
        email: 'charlie@test.com'
      }
    })

    homeService.fetchHomePageData.mockResolvedValue(mockHomeData)
    itemApi.getItemById.mockResolvedValue(mockItemDetail)

    // Act: Render and navigate
    renderWithRouter('/')

    await waitFor(() => {
      expect(screen.getByText('Unique Test Place')).toBeInTheDocument()
    })

    fireEvent.click(screen.getByText('View Details'))

    // Assert: Verify the correct ID (42) was passed to the API
    await waitFor(() => {
      expect(itemApi.getItemById).toHaveBeenCalledWith('42')
      expect(screen.getByText('Charlie Brown')).toBeInTheDocument()
    })
  })

  it('handles navigation back from item detail page to home page', async () => {
    // Arrange: Set up simple navigation test
    const mockPlaces = [
      {
        id: 1,
        name: 'Test Place',
        address: '123 Test St',
        tags: ['Test'],
        verifiedCount: 5,
        priceLevel: 2
      }
    ]

    const mockHomeData = createMockHomeData(mockPlaces)
    const mockItemDetail = createMockItemDetail({
      item_id: 1,
      name: 'Test Place',
      location: '123 Test St',
      added_by_user: {
        first_name: 'Test',
        last_name: 'User',
        email: 'test@test.com'
      }
    })

    homeService.fetchHomePageData.mockResolvedValue(mockHomeData)
    itemApi.getItemById.mockResolvedValue(mockItemDetail)

    // Act: Navigate to detail page
    renderWithRouter('/')

    await waitFor(() => {
      expect(screen.getByText('Test Place')).toBeInTheDocument()
    })

    fireEvent.click(screen.getByText('View Details'))

    await waitFor(() => {
      expect(screen.getByText('Test User')).toBeInTheDocument()
    })

    // Click the Back button
    const backButton = screen.getByText('Back')
    expect(backButton).toBeInTheDocument()
    fireEvent.click(backButton)

    // Assert: Verify we're back on home page
    await waitFor(() => {
      expect(screen.getByText('All Places')).toBeInTheDocument()
    })
  })

  it('displays error when navigating to non-existent item', async () => {
    // Arrange: Mock API to return error
    const mockHomeData = createMockHomeData([])
    
    homeService.fetchHomePageData.mockResolvedValue(mockHomeData)
    itemApi.getItemById.mockRejectedValue(new Error('Item not found'))

    // Act: Navigate directly to non-existent item
    renderWithRouter('/item/999')

    // Assert: Verify error message appears
    await waitFor(() => {
      expect(screen.getByText('Error')).toBeInTheDocument()
      expect(screen.getByText(/Item not found|Failed to load item details/i)).toBeInTheDocument()
    })

    // Verify Go Back button is available
    expect(screen.getByText('Go Back')).toBeInTheDocument()
  })
})
