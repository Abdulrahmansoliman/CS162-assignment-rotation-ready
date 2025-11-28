import { CITY_API_URL } from "../config/api";

export async function getCities() {
  const response = await fetch(CITY_API_URL, {
    method: "GET",
    credentials: "include",
  });

  if (!response.ok) throw new Error("Failed to fetch rotation cities");
  return response.json();
}
