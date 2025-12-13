import { apiFetch } from ".";

export async function getTags() {
  return await apiFetch("/tag/", {
    method: "GET",
  });
}


