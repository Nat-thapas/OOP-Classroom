<script lang="ts">
	import { onMount } from 'svelte';
    import { fade, scale } from 'svelte/transition';
    import { quadOut } from 'svelte/easing';

	const api_url: string = import.meta.env.VITE_API_URL;

	const token: string | null = localStorage.getItem('token');

    let is_create_or_join_menu_open: boolean = false;
    let is_join_class_menu_open: boolean = false;
    let is_create_class_menu_open: boolean = false;
    let is_user_menu_open: boolean = false;
    let is_edit_user_menu_open: boolean = false;

    let join_classroom_code: string;

    let create_classroom_name: string;
    let create_classroom_section: string;
    let create_classroom_subject: string;
    let create_classroom_room: string;

    let new_username: string;
    let new_email: string;
    let old_password: string;
    let new_password: string;

    function toggle_create_or_join_menu_state() {
        is_user_menu_open = false;
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

    function toggle_user_menu_state() {
        is_create_or_join_menu_open = false;
        is_user_menu_open = !is_user_menu_open;
    }

    function toggle_edit_user_menu_state() {
        is_user_menu_open = false;
        is_edit_user_menu_open = !is_edit_user_menu_open;
    }

    async function get_current_user(): Promise<any> {
        const response = await fetch(`${api_url}/users/@me`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        const response_data = await response.json();
        return response_data;
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

    async function logout() {
        localStorage.removeItem('token');
        window.location.href = '/login';
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

    async function edit_user() {
        if (new_username.length < 3 || new_username.length > 64) {
            alert("Username must be between 3 and 64 characters long");
            return;
        }
        if (old_password.length < 8 || old_password.length > 64) {
            alert("Password must be between 8 and 64 characters long");
            return;
        }
        if (new_password){
            if (new_password.length < 8 || new_password.length > 64) {
                alert("Password must be between 8 and 64 characters long");
                return;
            }
        }
        const response = await fetch(`${api_url}/users/@me`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: new_username,
                email: new_email,
                old_password: old_password,
                new_password: new_password || null
            })
        });
        const response_data = await response.json();
        if (response.status !== 200) {
            if (response.status !== 422) {
                alert(response_data.detail);
                return;
            }
            alert("Failed edit user");
            return;
        }
        alert("User edited successfully");
        window.location.reload();
    }

    async function join_classroom() {
        if (join_classroom_code.length !== 8) {
            alert("Class code must be 8 characters long");
            return;
        }
        join_classroom_code = join_classroom_code.toUpperCase();
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
        if (create_classroom_name.length > 48) {
            alert("Classname must be less than 48 characters long");
            return;
        }
        if (create_classroom_section && create_classroom_section.length > 16) {
            alert("Section must be less than 16 characters long");
            return;
        }
        if (create_classroom_subject && create_classroom_subject.length > 32) {
            alert("Subject must be less than 32 characters long");
            return;
        }
        if (create_classroom_room && create_classroom_room.length > 16) {
            alert("Room must be less than 16 characters long");
            return;
        }
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
        const user = await current_user;
        new_username = user.username;
        new_email = user.email;
    });

    let current_user: Promise<any> = get_current_user();
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
{#await current_user then current_user}
<button class="float-right" on:click={toggle_user_menu_state}>
    <img src="{api_url}/users/{current_user.id}/avatar/data" alt="Avatar" class="h-12 mt-2 mr-4 rounded-full cursor-pointer">
</button>
{/await}
{#if is_user_menu_open}
<div class="absolute top-10 right-8 w-fit h-28 bg-white border border-solid border-gray-300 rounded-lg drop-shadow-lg">
    <button class="block text-left w-32 h-12 pt-3 pb-5 pl-4 pr-4 mt-2 hover:bg-gray-100" on:click={toggle_edit_user_menu_state}>Edit</button>
    <button class="block text-left w-32 h-12 pt-3 pb-5 pl-4 pr-4 hover:bg-gray-100" on:click={logout}>Logout</button>
</div>
{/if}
{#if is_edit_user_menu_open}
<div transition:fade={{ duration: 150, easing: quadOut }} class="fixed top-0 left-0 bottom-0 right-0 bg-black opacity-50 z-40"></div>
    <div transition:scale={{ duration: 150, easing: quadOut, start: 0.75 }} class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[36rem] h-fit z-50 bg-white rounded-xl p-5">
        <h1 class="text-lg font-medium text-gray-600 inline-block">Edit user</h1>
        <button class="inline-block cursor-pointer float-right" on:click={() => {is_edit_user_menu_open = false;}}>
            <span class="material-symbols-outlined">
                close
            </span>
        </button>
        <form on:submit|preventDefault={edit_user} action="/edit_user" method="post">
            <input
                type="text"
                class="w-[32rem] h-12 m-auto mt-4 block p-5 rounded-t-md border-b bg-gray-100 border-solid border-black focus:border-b-2 focus:border-blue-700 outline-none placeholder:text-gray-500"
                required
                placeholder="Username"
                bind:value={new_username}
            />
            <input
                type="email"
                class="w-[32rem] h-12 m-auto mt-4 block p-5 rounded-t-md border-b bg-gray-100 border-solid border-black focus:border-b-2 focus:border-blue-700 outline-none placeholder:text-gray-500"
                required
                placeholder="Email"
                bind:value={new_email}
            />
            <input
                type="password"
                class="w-[32rem] h-12 m-auto mt-4 block p-5 rounded-t-md border-b bg-gray-100 border-solid border-black focus:border-b-2 focus:border-blue-700 outline-none placeholder:text-gray-500"
                required
                placeholder="Old password"
                bind:value={old_password}
            />
            <input
                type="password"
                class="w-[32rem] h-12 m-auto mt-4 mb-8 block p-5 rounded-t-md border-b bg-gray-100 border-solid border-black focus:border-b-2 focus:border-blue-700 outline-none placeholder:text-gray-500"
                placeholder="New password (optional)"
                bind:value={new_password}
            />
            <div>
                <button
                    type="submit"
                    class="w-[32rem] h-12 m-auto mt-4 block bg-blue-500 text-white rounded-full hover:bg-blue-600 hover:drop-shadow-md duration-100 ease-in"
                >
                    Edit
                </button>
            </div>
        </form>
    </div>
{/if}
    <button class="float-right m-1.5 mt-2 mr-4" on:click={toggle_create_or_join_menu_state}>
        <span class="material-symbols-outlined pt-1.5 pb-1.5 pl-2 pr-2 cursor-pointer rounded-full hover:bg-gray-100 text-3xl">
            add
        </span>
    </button>
{#if is_create_or_join_menu_open}
    <div class="absolute top-10 right-20 w-fit h-28 bg-white border border-solid border-gray-300 rounded-lg drop-shadow-lg">
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
                class="w-[32rem] h-12 m-auto mt-4 block p-5 uppercase rounded-md border border-solid border-gray-500 focus:border-blue-700 outline-none placeholder:text-gray-500"
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
{#await current_user then current_user}
    <div class="flex">
        <nav class="w-80 h-fit min-h-screen pt-2 border-r border-solid border-gray-300">
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
                    {#if classroom.owner.id === current_user.id}
                    <a href="/classrooms/{classroom.id}" class="h-fit cursor-pointer">
                        <div class="h-12 mt-2 mb-2 mr-3 rounded-r-full hover:bg-gray-100">
                            <div style="background-color: {classroom.theme_color};" class="h-8 w-8 relative -top-[1.125rem] left-3 text-lg font-semibold text-white rounded-full inline-flex items-center justify-center">
                                {classroom.name[0].toUpperCase()}
                            </div>
                            <div class="relative {classroom.section ? "top-0.5" : "top-2.5"} ml-6 w-56 font-medium inline-block text-gray-600 text-ellipsis text-nowrap overflow-hidden">
                                {classroom.name}
                                <br>
                                <span class="text-gray-500 font-normal text-sm w-56 relative -top-1.5 text-ellipsis text-nowrap overflow-hidden">
                                    {classroom.section || "⠀"}
                                </span>
                            </div>
                        </div>
                    </a>
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
                    {#if classroom.owner.id !== current_user.id}
                    <a href="/classrooms/{classroom.id}" class="h-fit cursor-pointer">
                        <div class="h-12 mt-2 mb-2 mr-3 rounded-r-full hover:bg-gray-100">
                            <div style="background-color: {classroom.theme_color};" class="h-8 w-8 relative -top-[1.125rem] left-3 text-lg font-semibold text-white rounded-full inline-flex items-center justify-center">
                                {classroom.name[0].toUpperCase()}
                            </div>
                            <div class="relative {classroom.section ? "top-0.5" : "top-2.5"} ml-6 w-56 font-medium inline-block text-gray-600 text-ellipsis text-nowrap overflow-hidden">
                                {classroom.name}
                                <br>
                                <span class="text-gray-500 font-normal text-sm w-56 relative -top-1.5 text-ellipsis text-nowrap overflow-hidden">
                                    {classroom.section || "⠀"}
                                </span>
                            </div>
                        </div>
                    </a>
                    {/if}
                {/each}
            {/await}
            <hr>
        </nav>
        <div style="width: calc(100vw - 24rem);" class="h-screen flex flex-wrap items-start content-start gap-0">
            {#await classrooms then classrooms}
                {#each classrooms as classroom (classroom.id)}
                    <a href="/classrooms/{classroom.id}" class="w-80 h-72 bg-white mt-6 ml-6 rounded-lg border border-solid border-gray-300 cursor-pointer hover:drop-shadow-xl">
                        <div style="background-image: url({api_url}/{classroom.banner_path}); background-repeat: no-repeat; background-size: 25rem 6.5rem" class="w-[19.9rem] bg-no-repeat px-4 py-3 rounded-t-lg">
                            <h1 class="text-2xl font-medium text-white text-ellipsis text-nowrap overflow-hidden">{classroom.name}</h1>
                            <p class="text-white text-sm text-ellipsis text-nowrap overflow-hidden">{classroom.section || "⠀"}</p>
                            <p class="text-white mt-1 text-ellipsis text-nowrap overflow-hidden">{classroom.owner.username}</p>
                            <img src="{api_url}/users/{classroom.owner.id}/avatar/data" alt="Avatar" class="w-20 h-20 relative -top-7 float-right rounded-full">
                        </div>
                    </a>
                {/each}
            {/await}
        </div>
    </div>
{/await}
