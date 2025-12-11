// frontend/src/api/otherUser.js
import { apiFetch } from "./index.js";

export async function getUserById(user_id) {
  return await apiFetch(`/user/${user_id}`, {
    method: "GET",
  });
}


