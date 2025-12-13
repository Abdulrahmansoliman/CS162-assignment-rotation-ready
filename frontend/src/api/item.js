import { apiFetch } from ".";

export async function createItem(body) {
  return await apiFetch("/item/", {
    method: "POST",
    body: JSON.stringify(body),
  });
}
