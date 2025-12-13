import { apiFetch } from "./index.js";

export async function getItems() {
  return await apiFetch("/item", {
    method: "GET",
  });
}

export async function getItemById(item_id) {
  return await apiFetch(`/item/${item_id}`, {
    method: "GET",
  });
}

export async function createItem(itemData) {
  return await apiFetch("/item", {
    method: "POST",
    body: JSON.stringify(itemData),
  });
}