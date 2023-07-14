import { streams, validLogin } from "$lib";
import { redirect } from "@sveltejs/kit";


// get readable stream for client
// check if user was logged in
// check credentials
// if so, return stream
export async function GET({ cookies }) {

    const cookie = cookies.get("login")
    if (!cookie) throw redirect(307, "/login")
    const { username, password } = JSON.parse(cookie)
    if (!username || !password) throw redirect(307, "/login")
    if (!validLogin(username, password)) throw redirect(307, "/login")

    let controller: ReadableStreamDefaultController | undefined;
    const stream = new ReadableStream({
        start(control) {
            controller = control;
            controller.enqueue(new TextEncoder().encode(": ping\n\n"));
            streams.add(controller);
        },

        cancel() {
            if (controller)
                streams.delete(controller);
        },
    });
    const response = new Response(stream, {
        headers: {
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    }); 

    return response;
}