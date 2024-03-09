<script lang="ts">
	import { onMount } from 'svelte';
    import { fade, scale } from 'svelte/transition';
    import { quadOut } from 'svelte/easing';

	const api_url: string = import.meta.env.VITE_API_URL;

	const token: string | null = localStorage.getItem('token');
    let current_user: any;

    let is_create_or_join_menu_open: boolean = false;
    let is_join_class_menu_open: boolean = false;
    let is_create_class_menu_open: boolean = false;

    let join_classroom_code: string;

    let create_classroom_name: string;
    let create_classroom_section: string;
    let create_classroom_subject: string;
    let create_classroom_room: string;

    function toggle_create_or_join_menu_state() {
        is_create_or_join_menu_open = !is_create_or_join_menu_open;
    }

    function toggle_join_class_menu_state() {
        is_create_or_join_menu_open = false;
        is_join_class_menu_open = !is_join_class_menu_open;
    }

    function toggle_create_class_menu_state() {
        is_create_or_join_menu_open = false;
        is_create_class_menu_open = !is_create_class_menu_open;
    }

    async function get_current_user() {
        const response = await fetch(`${api_url}/users/@me`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        const response_data = await response.json();
        current_user = response_data;
    }

    async function check_token(): Promise<boolean> {
        if (!token) {
            return false;
        }
        const response = await fetch(`${api_url}/auth/verify_token`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (response.status !== 200) {
            localStorage.removeItem('token');
            return false;
        }
        return true;
    }

    async function get_classrooms(): Promise<any> {
        const response = await fetch(`${api_url}/classrooms`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        const response_data = await response.json();
        return response_data;
    }

    async function join_classroom() {
        if (join_classroom_code.length !== 8) {
            alert("Class code must be 8 characters long");
            return;
        }
        const response = await fetch(`${api_url}/classrooms`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                classroom_code: join_classroom_code
            })
        });
        const response_data = await response.json();
        if (response.status !== 200) {
            if (response.status !== 422) {
                alert(response_data.detail);
                return;
            }
            alert("Failed to join classroom");
            return;
        }
        window.location.href = `/classrooms/${response_data.id}`;
    }

    async function create_classroom() {
        const response = await fetch(`${api_url}/classrooms`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: create_classroom_name,
                section: create_classroom_section || null,
                subject: create_classroom_subject || null,
                room: create_classroom_room || null
            })
        });
        const response_data = await response.json();
        if (response.status !== 201) {
            if (response.status !== 422) {
                alert(response_data.detail);
                return;
            }
            alert("Failed to create classroom");
            return;
        }
        window.location.href = `/classrooms/${response_data.id}`;
    }

    onMount(async () => {
        if (!await check_token()) {
            window.location.href = '/login';
        }
        await get_current_user();
    });

    let classrooms: Promise<any> = get_classrooms();
</script>

<svelte:head>
   <title>Classrooms</title>
</svelte:head>

<span class="material-symbols-outlined inline-block p-3 m-2 cursor-pointer rounded-full hover:bg-gray-100 text-gray-600">
    menu
</span>
<a href="/">
    <div class="h-8 inline-block cursor-pointer group -top-1 relative">
        <img src="/logo.svg" alt="Logo" class="float-left h-8 mt-3">
        <h1 class="inline-block text-2xl text-gray-600 mt-2.5 ml-2 group-hover:underline group-hover:text-green-700">Classroom</h1>
    </div>
</a>
<button class="float-right m-1.5 mt-2 mr-4" on:click={toggle_create_or_join_menu_state}>
    <span class="material-symbols-outlined pt-1.5 pb-1.5 pl-2 pr-2 cursor-pointer rounded-full hover:bg-gray-100 text-3xl">
        add
    </span>
</button>
{#if is_create_or_join_menu_open}
    <div class="absolute top-10 right-8 w-fit h-28 bg-white border border-solid border-gray-300 rounded-lg drop-shadow-lg">
        <button class="block text-left w-32 h-12 pt-3 pb-5 pl-4 pr-4 mt-2 hover:bg-gray-100" on:click={toggle_join_class_menu_state}>Join class</button>
        <button class="block text-left w-32 h-12 pt-3 pb-5 pl-4 pr-4 hover:bg-gray-100" on:click={toggle_create_class_menu_state}>Create class</button>
    </div>
{/if}
{#if is_join_class_menu_open}
    <div transition:fade={{ duration: 150, easing: quadOut }} class="fixed top-0 left-0 bottom-0 right-0 bg-black opacity-50 z-40"></div>
    <div transition:scale={{ duration: 150, easing: quadOut, start: 0.75 }} class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[36rem] h-fit z-50 bg-white rounded-xl p-5">
        <h1 class="text-lg font-medium text-gray-600 inline-block">Join class</h1>
        <button class="inline-block cursor-pointer float-right" on:click={() => {is_join_class_menu_open = false;}}>
            <span class="material-symbols-outlined">
                close
            </span>
        </button>
        <form on:submit|preventDefault={join_classroom} action="/join_classroom" method="post">
            <input
                type="text"
                class="w-[32rem] h-12 m-auto mt-4 block p-5 rounded-md border border-solid border-gray-500 focus:border-blue-700 outline-none placeholder:text-gray-500"
                required
                placeholder="Class code"
                bind:value={join_classroom_code}
            />
            <div>
                <button
                    type="submit"
                    class="w-[32rem] h-12 m-auto mt-4 block bg-blue-500 text-white rounded-full hover:bg-blue-600 hover:drop-shadow-md duration-100 ease-in"
                >
                    Join
                </button>
            </div>
        </form>
    </div>
{/if}
{#if is_create_class_menu_open}
    <div transition:fade={{ duration: 150, easing: quadOut }} class="fixed top-0 left-0 bottom-0 right-0 bg-black opacity-50 z-40"></div>
    <div transition:scale={{ duration: 150, easing: quadOut, start: 0.75 }} class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[36rem] h-fit z-50 bg-white rounded-xl p-5">
        <h1 class="text-lg font-medium text-gray-600 inline-block">Create class</h1>
        <button class="inline-block cursor-pointer float-right" on:click={() => {is_create_class_menu_open = false;}}>
            <span class="material-symbols-outlined">
                close
            </span>
        </button>
        <form on:submit|preventDefault={create_classroom} action="/create_classroom" method="post">
            <input
                type="text"
                class="w-[32rem] h-12 m-auto mt-4 block p-5 rounded-t-md border-b bg-gray-100 border-solid border-black focus:border-b-2 focus:border-blue-700 outline-none placeholder:text-gray-500"
                required
                placeholder="Classname (required)"
                bind:value={create_classroom_name}
            />
            <input
                type="text"
                class="w-[32rem] h-12 m-auto mt-4 block p-5 rounded-t-md border-b bg-gray-100 border-solid border-black focus:border-b-2 focus:border-blue-700 outline-none placeholder:text-gray-500"
                placeholder="Section"
                bind:value={create_classroom_section}
            />
            <input
                type="text"
                class="w-[32rem] h-12 m-auto mt-4 block p-5 rounded-t-md border-b bg-gray-100 border-solid border-black focus:border-b-2 focus:border-blue-700 outline-none placeholder:text-gray-500"
                placeholder="Subject"
                bind:value={create_classroom_subject}
            />
            <input
                type="text"
                class="w-[32rem] h-12 m-auto mt-4 mb-8 block p-5 rounded-t-md border-b bg-gray-100 border-solid border-black focus:border-b-2 focus:border-blue-700 outline-none placeholder:text-gray-500"
                placeholder="Room"
                bind:value={create_classroom_room}
            />
            <div>
                <button
                    type="submit"
                    class="w-[32rem] h-12 m-auto mt-4 block bg-blue-500 text-white rounded-full hover:bg-blue-600 hover:drop-shadow-md duration-100 ease-in"
                >
                    Create
                </button>
            </div>
        </form>
    </div>
{/if}
<hr class="mb-0">
<div class="flex">
    <nav class="w-80 h-screen pt-2 border-r border-solid border-gray-300">
        <div class="h-10 mt-0 mb-2 mr-3 rounded-r-full hover:bg-gray-100 cursor-pointer">
            <span class="material-symbols-outlined mt-2 ml-4 inline-block text-gray-600">
                home
            </span>
            <span class="relative -top-1.5 ml-4 font-medium inline-block text-gray-600">
                Home
            </span>
        </div>
        <hr>
        <div class="h-10 mt-2 mb-2 mr-3 rounded-r-full hover:bg-gray-100 cursor-pointer">
            <span class="material-symbols-outlined mt-2 ml-4 inline-block text-gray-600">
                group
            </span>
            <span class="relative -top-1.5 ml-4 font-medium inline-block text-gray-600">
                Teaching
            </span>
        </div>
        {#await classrooms then classrooms}
            {#each classrooms as classroom (classroom.id)}
                {#if classroom.owner_id === current_user.id}
                <div class="h-12 mt-2 mb-2 mr-3 rounded-r-full hover:bg-gray-100 cursor-pointer">
                    <span style="background-color: {classroom.theme_color};" class="mt-2 ml-[1.125rem] mr-0 text-lg font-semibold rounded-full pt-0.5 pb-0.5 pl-3 pr-3 relative -top-3 -left-2 inline-block text-white">
                        {classroom.name[0]}
                    </span>
                    <span class="relative top-0.5 ml-0.5 font-medium inline-block text-gray-600">
                        {classroom.name}
                        <br>
                        <span class="text-gray-500 font-normal text-sm relative -top-1.5">
                            {classroom.section || "No section"}
                        </span>
                    </span>
                </div>
                {/if}
            {/each}
        {/await}
        <hr>
        <div class="h-10 mt-2 mb-2 mr-3 rounded-r-full hover:bg-gray-100 cursor-pointer">
            <span class="material-symbols-outlined mt-2 ml-4 inline-block text-gray-600">
                school
                </span>
            <span class="relative -top-1.5 ml-4 font-medium inline-block text-gray-600">
                Enrolled
            </span>
        </div>
        {#await classrooms then classrooms}
            {#each classrooms as classroom (classroom.id)}
                {#if classroom.owner_id !== current_user.id}
                <div class="h-12 mt-2 mb-2 mr-3 rounded-r-full hover:bg-gray-100 cursor-pointer">
                    <span class="mt-2 ml-[1.125rem] mr-0 text-lg font-semibold rounded-full pt-0.5 pb-0.5 pl-3 pr-3 relative -top-3 -left-2 bg-blue-400 inline-block text-white">
                        {classroom.name[0]}
                    </span>
                    <span class="relative top-0.5 ml-0.5 font-medium inline-block text-gray-600">
                        {classroom.name}
                        <br>
                        <span class="text-gray-500 font-normal text-sm relative -top-1.5">
                            {classroom.section}
                        </span>
                    </span>
                </div>
                {/if}
            {/each}
        {/await}
        <hr>
    </nav>
    <div class="h-screen">
        {#await classrooms then classrooms}
            {#each classrooms as classroom (classroom.id)}
                <div class="">
                    <h1 class="text-3xl mt-8 text-center">{classroom.name}</h1>
                    <p class="text-center mt-4">{classroom.description}</p>
                </div>
            {/each}
        {/await}
    </div>
</div>
