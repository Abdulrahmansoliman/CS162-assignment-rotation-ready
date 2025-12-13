import { apiFetch } from "./index";

export async function getItems() {
    return await apiFetch("/item/", { 
        method: "GET"
    });
}
