import apiFetch from "./apiFetch";

export async function getTags() {
  return apiFetch("/api/v1/tag/");
}


