import apiFetch from "./index.js";

export async function getUserById(user_id) {
  return apiFetch(`/api/v1/user/${user_id}`);
}
