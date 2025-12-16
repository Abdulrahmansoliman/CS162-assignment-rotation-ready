import { apiFetch } from ".";

export async function getItems() {
  return await apiFetch("/item/", {
    method: "GET",
  });
}

export async function getItemById(item_id) {
  return await apiFetch(`/item/${item_id}`, {
    method: "GET",
  });
}

export async function createItem(body) {
  return await apiFetch("/item/", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

/**
 * Fetch items contributed by a specific user
 */
export async function getUserItems(userId) {
  return await apiFetch(`/item/user/${userId}`, {
    method: "GET",
  });
}

