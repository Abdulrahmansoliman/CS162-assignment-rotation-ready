import { apiFetch } from ".";

/**
 * Fetch all items for the current user's rotation city.
 * 
 * Retrieves all items shared by students in the authenticated user's city.
 * Items are filtered by rotation_city_id extracted from JWT token.
 * Requires authentication.
 * 
 * @returns {Promise<Array<Object>>} Array of item objects with details, categories, and tags
 * @throws {Error} If API request fails or user is not authenticated
 */
export async function getItems() {
  return await apiFetch("/item/", {
    method: "GET",
  });
}

/**
 * Fetch a specific item by ID.
 * 
 * Retrieves detailed information about a single item including categories,
 * tags, and verification history. Item must belong to user's rotation city.
 * Requires authentication.
 * 
 * @param {number} item_id - The ID of the item to retrieve
 * @returns {Promise<Object>} Item object with full details
 * @throws {Error} If item not found, doesn't belong to user's city, or authentication fails
 */
export async function getItemById(item_id) {
  return await apiFetch(`/item/${item_id}`, {
    method: "GET",
  });
}

/**
 * Create a new item with categories and tags.
 * 
 * Creates a new item in the user's rotation city. User's city is automatically
 * assigned from JWT token. At least one category is required.
 * Requires authentication.
 * 
 * @param {Object} body - Item creation data
 * @param {string} body.name - Item name
 * @param {string} body.location - Physical location description
 * @param {number} [body.walking_distance] - Optional walking distance in meters
 * @param {Array<number>} body.category_ids - Array of category IDs (at least one required)
 * @param {Array<Object>} body.existing_tags - Array of {tag_id, value} for existing tags
 * @param {Array<Object>} body.new_tags - Array of {name, value_type, value} for new tags
 * @returns {Promise<Object>} Created item object
 * @throws {Error} If validation fails, user has no rotation city, or authentication fails
 */
export async function createItem(body) {
  return await apiFetch("/item/", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

/**
 * Fetch items contributed by a specific user.
 * 
 * Retrieves all items added by a specific user in the current user's rotation city.
 * Requires authentication.
 * 
 * @param {number} userId - The ID of the user whose items to retrieve
 * @returns {Promise<Array<Object>>} Array of item objects created by the specified user
 * @throws {Error} If API request fails or user is not authenticated
 */
export async function getUserItems(userId) {
  return await apiFetch(`/item/user/${userId}`, {
    method: "GET",
  });
}

