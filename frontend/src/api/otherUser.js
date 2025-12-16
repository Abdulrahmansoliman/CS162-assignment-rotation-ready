// frontend/src/api/otherUser.js
import { apiFetch } from "./index.js";

/**
 * Fetch a specific user's public profile by ID.
 * 
 * Retrieves public profile information for any user in the system.
 * Useful for displaying user information on items and verifications.
 * Requires authentication.
 * 
 * @param {number} user_id - The ID of the user to retrieve
 * @returns {Promise<{user_id: number, first_name: string, last_name: string, email: string, rotation_city: Object}>} User profile object
 * @throws {Error} If user not found or authentication fails
 */
export async function getUserById(user_id) {
  return await apiFetch(`/user/${user_id}`, {
    method: "GET",
  });
}


