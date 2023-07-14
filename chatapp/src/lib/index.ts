export interface Message {
    content: string;
    author: string;
    id: string;
    timestamp: string;
}

// map of users
/** key: username, value: password */
export const users = new Map<string, string>();

// map of messages
export const messages = new Map<string, Message>();

// set of all streams
export const streams = new Set<ReadableStreamDefaultController>();

// broadcast message to all clients(aka. streams)
export const broadcast = (message: unknown) => {
    for (const stream of streams) {
        stream.enqueue(new TextEncoder().encode(`data: ${JSON.stringify(message)}\n\n`));
    }
};

// check if user exists and if password is correct
export function validLogin(username:string, password:string) {
    if (users.has(username)) {
        return users.get(username) === password;
    }
    return false;
}

// create user
export function createUser(username:string, password:string) {
    if (users.has(username) || username === "" || password === "" || username == "server") {
        return false;
    }
    users.set(username, password);
    return true;
}

// add a guest user
users.set("guest", "guest");
// add a message when starting the server
messages.set("0", {content: "Server started!", author: "server", id: "1", timestamp: new Date().toLocaleTimeString()});