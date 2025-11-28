import { apiFetch } from ".";

export async function getCurrentUser() {
  const response = await apiFetch("user/me", { method: "GET" });

  if (!response.ok) {
    throw new Error("Failed to fetch user");
  }

  return response.json();
}

export async function updateUserProfile(data) {
  const response = await apiFetch("user/me", {
    method: "PUT",
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("Failed to update user profile");
  }

  return response.json();
}
