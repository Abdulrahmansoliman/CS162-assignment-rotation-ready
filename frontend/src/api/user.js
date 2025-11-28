import { API_BASE_URL } from "../config/api";

// GET CURRENT USER PROFILE
export async function getCurrentUser() {
  const response = await fetch(`${API_BASE_URL}/me`, {
    method: "GET",
    credentials: "include",  // required for JWT cookies
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) throw new Error("Failed to fetch user profile");
  return response.json();
}

// UPDATE CURRENT USER PROFILE
export async function updateUserProfile(payload) {
  const response = await fetch(`${API_BASE_URL}/me`, {
    method: "PUT",
    credentials: "include", // required for JWT cookies
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) throw new Error("Failed to update profile");
  return response.json();
}
