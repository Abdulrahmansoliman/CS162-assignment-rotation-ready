import { apiFetch } from ".";

export async function getCities() {
  return await apiFetch("rotation-city", {
    method: "GET",
  });
}


