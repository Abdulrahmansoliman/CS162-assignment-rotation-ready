import { apiFetch } from ".";

export async function getCategories() {
  return await apiFetch("/category/", {
    method: "GET",
  });
}


