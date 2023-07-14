import { validLogin } from '$lib';
import { redirect } from '@sveltejs/kit';


// check if user was logged in
// if so, DONT redirect to /login
// return username and password
export function load({ cookies }) {

    let cookie:any= cookies.get("login");
    
    if (!cookie) throw redirect(307, "/login");
    
    cookie = JSON.parse(cookie)

    if (!cookie) throw redirect(307, "/login");

    const username = cookie.username
    const password = cookie.password

    if (!username || !password) {
        cookies.delete("login")
        throw redirect(307, "/login")
    };

    if (!validLogin(username, password)) {
        cookies.delete("login")
        throw redirect(307, "/login")
    }

    return { username, password };
}

// idk, when this wasnt here, you somewhy needed to refresh the page to not get an error
export const actions = {
	default: async ({ request, cookies }) => {}
};