import { apiFetch } from ".";

/**
 * Fetch verification history for a specific item.
 * 
 * Retrieves all verifications for an item, showing who verified it and when.
 * Results are paginated with the specified limit.
 * Requires authentication.
 * 
 * @param {number} itemId - The ID of the item to get verifications for
 * @param {number} [limit=50] - Maximum number of verifications to retrieve
 * @returns {Promise<Array<{verification_id: number, user: Object, verified_at: string, note: string|null}>>} Array of verification objects
 * @throws {Error} If item not found or authentication fails
 */
export async function getItemVerifications(itemId, limit = 50) {
  return await apiFetch(`/verification/items/${itemId}?limit=${limit}`, {
    method: "GET",
  });
}

/**
 * Create a verification for an item.
 * 
 * Verifies that an item exists and is still available. Users can only
 * verify an item once per day. Updates the item's verification count
 * and last verified date.
 * Requires authentication.
 * 
 * @param {number} itemId - The ID of the item to verify
 * @param {string} [note] - Optional note about the verification
 * @returns {Promise<{verification_id: number, message: string}>} Verification creation response
 * @throws {Error} If item not found, already verified today, or authentication fails
 */
export async function verifyItem(itemId, note) {
  return await apiFetch(`/verification/items/${itemId}`, {
    method: "POST",
    body: JSON.stringify(note ? { note } : {}),
  });
}


