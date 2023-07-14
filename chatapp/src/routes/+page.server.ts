import { redirect } from "@sveltejs/kit";

// Redirect to login page
// when loading /
export function load() {
    throw redirect(307, "/login");
}