import apiFetch from "./apiFetch";

export async function getCategories() {
  return apiFetch("/api/v1/category/");
}


