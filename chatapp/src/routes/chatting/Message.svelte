<script lang="ts">
    export let timestamp:string;
    export let content:string;
    export let author:string;
    export let user:string;

    const isServer = author === "server"
    const isUser = author === user

</script>

<div class="msg server user" style="display: none;" />

{#if isServer}
    <div class="server">
        <h class="date">{timestamp}</h>
        <h class="content">{content}</h>
    </div>
{:else if isUser}
    <div class="user">
        <h class="username">{author}</h>
        <h class="date">{timestamp}</h>
        <h class="content">{content}</h>
    </div>
{:else}
    <div class="message">
        <h class="username">{author}</h>
        <h class="date">{timestamp}</h>
        <h class="content">{content}</h>
    </div>
{/if}



<style>
    .server {
        width: 80%;
        padding: 10px;
        margin: 10px;
        margin-left: 10%;
        
        border-radius: 8px;
        border-style: solid;
        border-width: 1px;
        border-color: rgb(255, 255, 255, 0.2);
        
        background-color: rgb(255, 255, 255, 0.1);

        display: grid; 
        grid-template-columns: 1fr; 
        grid-template-rows: 1fr 1fr; 
        gap: 0px 0px; 
        grid-template-areas: 
            "date"
            "content"; 
        color:white;
    }
    .server .date {
        justify-self: center; 
        align-self: end; 
        grid-area: date; 
    }
    .server .content {
        justify-self: center; 
        align-self: start; 
        grid-area: content; 
    }

    .user {
        width: 50%;
        padding: 10px;
        margin: 10px;
        margin-left: 40%;

        border-radius: 8px;
        border-style: solid;
        border-width: 1px;
        border-color: rgb(255, 255, 255, 0.2);

        background-color: rgb(255, 200, 200, 0.1);


        display: grid; 
        grid-auto-columns: 1fr; 
        grid-template-columns: 1fr 1fr; 
        grid-template-rows: 1fr 1fr; 
        gap: 0px 0px; 
        grid-template-areas: 
            "date username"
            "content content"; 

        color:white;
    }
    .user .username {
        justify-self: end; 
        align-self: start; 
        grid-area: username; 
    }
    .user .date {
        justify-self: start; 
        align-self: start; 
        grid-area: date; 
    }
    .user .content {
        justify-self: end; 
        align-self: start; 
        grid-area: content; 
    }

    .message {
        width: 50%;
        padding: 10px;
        margin: 10px;
        margin-left: 10%;

        border-radius: 8px;
        border-style: solid;
        border-width: 1px;
        border-color: rgb(255, 255, 255, 0.2);

        background-color: rgb(200, 200, 255, 0.1);


        display: grid; 
        grid-auto-columns: 1fr; 
        grid-template-columns: 1fr 1fr; 
        grid-template-rows: 1fr 1fr; 
        gap: 0px 0px; 
        grid-template-areas: 
            "username date"
            "content content"; 

        color: white
    }
    .message .username {
        justify-self: start; 
        align-self: start; 
        grid-area: username; 
    }
    .message .date {
        justify-self: end; 
        align-self: start; 
        grid-area: date; 
    }
    .message .content {
        justify-self: start; 
        align-self: start; 
        grid-area: content; 
    }

</style>