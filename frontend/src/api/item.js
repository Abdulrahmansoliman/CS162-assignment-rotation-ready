import apiFetch from "./apiFetch";

export async function createItem(body) {
  return apiFetch("/api/v1/item", {
    method: "POST",
    body: JSON.stringify(body),
  });
}


