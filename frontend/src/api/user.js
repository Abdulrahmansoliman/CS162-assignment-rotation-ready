import { apiFetch } from ".";

/**
 * Fetch the current authenticated user's profile.
 * 
 * Retrieves the profile information for the currently logged-in user
 * including name, email, rotation city, and profile picture.
 * Requires authentication.
 * 
 * @returns {Promise<{user_id: number, first_name: string, last_name: string, email: string, rotation_city: Object, profile_picture: string|null}>} User profile object
 * @throws {Error} If authentication fails or user not found
 */
export async function getCurrentUser() {
  return await apiFetch("/user/me", {
    method: "GET",
  });
}

/**
 * Update the current user's profile.
 * 
 * Updates user profile fields. Only provided fields will be updated.
 * Requires authentication.
 * 
 * @param {Object} data - Profile update data
 * @param {string} [data.first_name] - User's first name
 * @param {string} [data.last_name] - User's last name
 * @param {number} [data.rotation_city_id] - New rotation city ID
 * @param {string} [data.profile_picture] - Base64 encoded profile picture
 * @returns {Promise<Object>} Updated user profile object
 * @throws {Error} If validation fails or authentication fails
 */
export async function updateUserProfile(data) {
  return await apiFetch("/user/me", {
    method: "PUT",
    body: JSON.stringify(data),
  });
}

