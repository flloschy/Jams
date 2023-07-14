import { broadcast, messages, validLogin } from "$lib";
import { redirect } from "@sveltejs/kit";

// receive new message from client
// check if user credentials are valid
// if so, broadcast message to all clients
export async function POST ({ request }) {
    const { content, author, password } = await request.json();
    
    if (!validLogin(author, password)) return new Response(JSON.stringify({ error: "Invalid credentials" }), { status: 400 });

    const id = Math.random().toString(16).slice(2);
    if (typeof content !== "string" || typeof author !== "string") {
        return new Response(JSON.stringify({ error: "Invalid message" }), { status: 400 });
    }
    messages.set(id, { content, author, id, timestamp: new Date().toLocaleTimeString() });
    broadcast({ id, content, author, timestamp: new Date().toLocaleTimeString() });
    return new Response(JSON.stringify({ id }));
}

// when loading chat history
// check if user credentials are valid
// if so, return all messages
export async function GET({ cookies }) {
    const cookie = cookies.get("login")
    if (!cookie) throw redirect(307, "/login")
    const { username, password } = JSON.parse(cookie)
    if (!username || !password) throw redirect(307, "/login")
    if (!validLogin(username, password)) throw redirect(307, "/login")
    
    const id = Math.random().toString(16).slice(2);
    broadcast({ id, content: `${username} has joined the chat`, author: "server", timestamp: new Date().toLocaleTimeString() });
    
    return new Response(JSON.stringify([...messages.values()]));
}