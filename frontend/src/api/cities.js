import { apiFetch } from ".";

/**
 * Fetch all available Minerva rotation cities.
 * 
 * Retrieves the list of all rotation cities where students can be located.
 * This is a public endpoint that does not require authentication.
 * 
 * @returns {Promise<Array<{city_id: number, name: string, country: string}>>} Array of rotation city objects
 * @throws {Error} If API request fails
 */
export async function getCities() {
  return await apiFetch("/rotation-city", {
    method: "GET",
  });
}


