import { apiFetch } from "@/api/index"

export const placeService = {
  async getPlaces(categoryId = null, searchQuery = null) {
    const params = new URLSearchParams()
    if (categoryId) params.append('category_id', categoryId)
    if (searchQuery) params.append('search', searchQuery)
    
    const queryString = params.toString()
    const url = queryString ? `/item/?${queryString}` : '/item/'
    return apiFetch(url)
  },

  async getCategories() {
    return apiFetch("/item/categories")
  },
}

