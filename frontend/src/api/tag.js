import { apiFetch } from ".";

/**
 * Fetch all available tags.
 * 
 * Retrieves all tags that can be applied to items (e.g., "Price", "Wifi", "Pet Friendly").
 * Tags have different value types (boolean, text, numeric).
 * Requires authentication.
 * 
 * @returns {Promise<Array<{tag_id: number, tag_name: string, value_type: number}>>} Array of tag objects
 * @throws {Error} If API request fails or user is not authenticated
 */
export async function getTags() {
  return await apiFetch("/tag/", {
    method: "GET",
  });
}


