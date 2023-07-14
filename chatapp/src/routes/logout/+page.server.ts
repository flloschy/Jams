import { redirect } from "@sveltejs/kit"

// Delete cookie and redirect to login page
// when loading /logout
export function load ({ cookies }) {
    cookies.delete("login")
    throw redirect(307, "/login")
}