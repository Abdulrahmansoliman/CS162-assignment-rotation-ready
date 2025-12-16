import { apiFetch } from ".";

/**
 * Fetch all available categories.
 * 
 * Retrieves all item categories from the API for organizing items.
 * Requires authentication.
 * 
 * @returns {Promise<Array<{category_id: number, category_name: string, category_pic: string}>>} Array of category objects
 * @throws {Error} If API request fails or user is not authenticated
 */
export async function getCategories() {
  return await apiFetch("/category/", {
    method: "GET",
  });
}


