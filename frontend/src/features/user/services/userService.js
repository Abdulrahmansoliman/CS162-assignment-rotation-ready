import { apiFetch } from "@/api/index"

export const userService = {
  async getCurrentUser() {
    return apiFetch("/user/me")
  },
}

