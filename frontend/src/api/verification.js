import { apiFetch } from ".";

export async function getItemVerifications(itemId, limit = 50) {
  return await apiFetch(`/verification/items/${itemId}?limit=${limit}`, {
    method: "GET",
  });
}

export async function verifyItem(itemId, note) {
  return await apiFetch(`/verification/items/${itemId}`, {
    method: "POST",
    body: JSON.stringify(note ? { note } : {}),
  });
}


