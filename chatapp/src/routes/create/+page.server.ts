import { createUser, validLogin } from '$lib'
import { redirect } from '@sveltejs/kit'


// check if user was logged in
// if so, redirect to /chatting
export function load ({cookies}) {

    const cookie = cookies.get("login")
    if (cookie) {
        const { username, password } = JSON.parse(cookie)
        if (username && password) {
            if (validLogin(username, password)) {
                throw redirect(307, "/chatting")
            }
        }
        cookies.delete("login")
    }
}

// when creating an account, check if username and password are valid
// create user and set cookie and redirect to /chatting
export const actions = {
	default: async ({ request, cookies }) => {
		const data = await request.formData();
        const username = data.get("username");
        const password = data.get("password");
        if (username && password) {
            const reply = createUser(username.toString(), password.toString())
            if (reply) {
                cookies.set("login", JSON.stringify({ username:username.toString(), password:password.toString() }))
                throw redirect(307, "/chatting")
            }
            return {
                fail: true,
            }
        }
    }
};