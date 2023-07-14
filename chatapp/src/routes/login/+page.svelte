<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

    export let form;

    let willShake = false
    let shake = () => {willShake = true; return ""};

    onMount(() => {
        shake = () => {
            const forum = document.getElementById("input")
            const currentColor = forum?.style.borderColor
            forum?.animate([
                { "borderColor": currentColor },
                { "borderColor": "red" },
                { "borderColor": currentColor }
            ], {duration: 500})
            return ""
        }
        if (willShake) shake()
    })
      
</script>

<form method="post" id="input">
    <label>
        <input name="username" type="text" placeholder="Username">
    </label><br>
    <label>
        <input name="password" type="password" placeholder="Password">
    </label><br>
    <button>login</button>
    <button on:click={
        async (e) => {
            e.preventDefault()
            goto("/create")
        }
    }>create an account</button>
</form>

<!-- make border red when login failed -->
{form?.fail ? shake() : ""}


<style>
    form {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: fit-content;
        height: fit-content;
    
        border-radius: 25px;
        border-style: solid;
        border-color: rgb(118, 118, 118);
        padding: 50px;
    }
    button {
        margin-top: 10px; 
        margin-bottom: 10px;   
        
        width: calc(100% + 30px);
        height: 25px;
        border-radius: 25px;
        
        padding-left: 15px;
        padding-right: 15px;

        transform: translate(-15px, 0);

        font-size: 15px;
        
        background-color: transparent;
        border-style: solid;
        border-color: rgb(118, 118, 118);
        color:rgb(118, 118, 118)

        
    }

    input {
        margin-top: 10px; 
        margin-bottom: 10px;   
        
        width: 100%;
        height: 25px;
        border-radius: 25px;
        
        padding-left: 15px;
        padding-right: 15px;

        transform: translate(-15px, 0);

        font-size: 15px;
        
        background-color: transparent;
        border-style: solid;
        color:rgb(118, 118, 118)
    }
    input:focus-within {
        outline: none;
    }

    button:focus-within {
        background-color: rgb(118, 118, 118);
        color: rgb(55, 55, 64);
    }
</style>