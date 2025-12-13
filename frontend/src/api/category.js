import { apiFetch } from "./index";

export async function getCategories() {
    return await apiFetch("/category/", {
        method: "GET"
    });
}
