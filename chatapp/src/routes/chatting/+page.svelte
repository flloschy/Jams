<script lang="ts">
	import { onMount } from "svelte";
    import Message from "./Message.svelte";

    export let data;

    interface Message {
        content: string;
        author: string;
        timestamp: string;
    }

    let chat:Message[] = []

    let chatbox:any;

    // scroll to the bottom of the chatbox
    const scrollDown = async () => {
        // wait for the DOM to update
        await new Promise((resolve) => setTimeout(resolve, 100))
        chatbox.scrollTop = chatbox.scrollHeight
    }

    onMount(async () => {
        chatbox = document.getElementById("chatbox")
        if (!chatbox) return

        // load chat history
        chat = await (await fetch("/api")).json() as Message[]
        // Send (client only) welcome message
        chat.push(
            {
                content: `Welcome to the chat ${data.username}!`,
                author: "server",
                timestamp: new Date().toLocaleTimeString()
            }
        )

        // get new messages
        const chatStream = new EventSource("/api/stream")
        chatStream.onmessage = async (event:MessageEvent) => {
            // append message to chat and scroll down
            const message = JSON.parse(event.data) as Message
            chat = chat.concat(message)

            scrollDown()
        }

        scrollDown()
    })

</script>


<a href="/logout" class="logout">Logout</a>

<div class="chatbox" id="chatbox">
    {#each chat as message}
        <Message author={message.author} content={message.content} timestamp={message.timestamp} user={data.username}></Message>
    {/each}
</div>

<input
    placeholder="send a message..."
    type="text"
    class="input"
    id="input"
    on:keydown={
        async (e) => {
            if (e.key === "Enter") {
                // Send message to server
                await fetch("/api", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        content: e.currentTarget.value,
                        author: data.username,
                        password: data.password
                    })
                })
                // @ts-ignore
                document.getElementById("input").value = ""
            }
        }
    }
/>



<style>
    .chatbox {
        margin-top: 2vh;
        width: 80%;
        height: 90vh;
        overflow-y: scroll;
        margin-left: 10%;
    }
    .input {
        width: 50%;
        height: 25px;
        border-radius: 25px;
        
        padding-left: 15px;
        padding-right: 15px;

        font-size: 15px;

        margin: 10px;
        margin-left: 25%;
        background-color: transparent;
        border-style: solid;
        color:rgb(118, 118, 118)
    }
    .input:focus-within {
        outline: none;
    }
    .logout {
        position: absolute;
        right: 0;
        top: 0;
        margin: 10px;
        padding: 10px;
        border-radius: 10px;
        text-decoration: none;
        color:rgb(118, 118, 118);
        background-color: transparent;
    }
    .chatbox::-webkit-scrollbar {
        display: none;
    }
</style>