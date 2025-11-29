import { apiFetch } from ".";

export async function getCurrentUser() {
  return await apiFetch("user/me", {
    method: "GET",
  });
}

export async function updateUserProfile(data) {
  return await apiFetch("user/me", {
    method: "PUT",
    body: JSON.stringify(data),
  });
}

