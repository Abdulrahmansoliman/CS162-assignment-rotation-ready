/**
 * Home Service
 * 
 * Service functions for the home page data fetching.
 * Handles user, categories, and items data transformation.
 */

import { getCurrentUser } from "../../../api/user";
import { getCategories } from "../../../api/category";
import { getItems } from "../../../api/item";
import { getLocaleFromCity, getUserDisplayName } from "../../../config/localeConfig";

/**
 * Fetch and transform user data for home page
 * @returns {Promise<{userName: string, locale: object}>}
 */
export async function fetchHomeUserData() {
    const user = await getCurrentUser();
    
    return {
        userName: getUserDisplayName(user),
        locale: getLocaleFromCity(user.rotation_city?.name)
    };
}

/**
 * Fetch and transform categories for home page
 * @returns {Promise<Array<{id: number, name: string, image: string|null}>>}
 */
export async function fetchCategories() {
    const categories = await getCategories();
    
    return categories.map(c => ({
        id: c.category_id,
        name: c.category_name,
        image: c.category_pic || null
    }));
}

/**
 * Fetch and transform items/places for home page
 * @returns {Promise<Array<{id: number, name: string, address: string, distance: string|null, tags: string[], verifiedCount: number, lastVerified: string|null, priceLevel: number}>>}
 */
export async function fetchPlaces() {
    const items = await getItems();
    
    return items.map(item => ({
        id: item.item_id,
        name: item.name,
        address: item.location,
        distance: item.walking_distance 
            ? (item.walking_distance / 1000).toFixed(1) 
            : null,
        tags: (item.tags || []).map(t => t.tag_name || t.name),
        verifiedCount: item.number_of_verifications || 0,
        lastVerified: item.created_at 
            ? new Date(item.created_at).toLocaleDateString() 
            : null,
        priceLevel: 1
    }));
}

/**
 * Fetch all home page data in parallel
 * @returns {Promise<{userName: string, locale: object, categories: Array, places: Array}>}
 */
export async function fetchHomePageData() {
    const [userData, categories, places] = await Promise.all([
        fetchHomeUserData(),
        fetchCategories(),
        fetchPlaces()
    ]);

    return {
        userName: userData.userName,
        locale: userData.locale,
        categories,
        places
    };
}
