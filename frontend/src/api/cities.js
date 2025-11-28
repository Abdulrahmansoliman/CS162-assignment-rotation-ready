import { apiFetch } from ".";

export async function getCities() {
  const response = await apiFetch("rotation-city", {
    method: "GET",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch cities");
  }

  return response.json();
}

