<script lang="ts">
    import { fade, scale } from 'svelte/transition';
    import { quadOut } from 'svelte/easing';

    export let data;

    const classroom_id: string = data.classroom_id;

    const api_url: string = import.meta.env.VITE_API_URL;

	const token: string | null = localStorage.getItem('token');

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

    async function get_current_classroom(): Promise<any> {
        const response = await fetch(`${api_url}/classrooms/${classroom_id}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        const response_data = await response.json();
        document.title = "Classworks - " + response_data.name;
        return response_data;
    }

    let current_user: Promise<any> = get_current_user();
    let current_classroom: Promise<any> = get_current_classroom();

    let is_create_classwork_menu_open: boolean = false;
    let is_create_topic_menu_open: boolean = false;

    function toggle_create_classwork_menu_state() {
        is_create_topic_menu_open = false;
        is_create_classwork_menu_open = !is_create_classwork_menu_open;
    }

    function toggle_create_topic_menu_state() {
        is_create_classwork_menu_open = false;
        is_create_topic_menu_open = !is_create_topic_menu_open;
    }

    let new_topic_name: string;

    async function create_topic() {
        if (new_topic_name.length > 64) {
            alert("Topic name must be less than 64 characters long.");
            return;
        }
        const response = await fetch(`${api_url}/classrooms/${classroom_id}/topics`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: new_topic_name
            })
        });
        const response_data = await response.json();
        is_create_topic_menu_open = false;
        current_user = get_current_user();
        current_classroom = get_current_classroom();
    }

    let item_type: any;
    let item_attachments: any;
    let item_topic: any;
    let item_title: string;
    let item_description: string;
    let item_due_date: string;
    let item_point: number;
    let item_option_1: string;
    let item_option_2: string;
    let item_option_3: string;
    let item_option_4: string;

    async function create_class_item() {
        if (item_title.length > 256) {
            alert("Title must be less than 256 characters long.");
            return;
        }
        if (item_description && item_description.length > 2048) {
            alert("Description must be less than 2048 characters long.");
            return;
        }
        if (item_point < 0) {
            alert("Points must be a positive number.");
            return;
        }
        const item_choices = [item_option_1, item_option_2, item_option_3, item_option_4].filter(Boolean)
        if (item_type === "MultipleChoiceQuestion" && item_choices.length < 2) {
            alert("Multiple choice questions must have at least 2 options.");
            return;
        }
        if (item_attachments && item_attachments.length > 8) {
            alert("You can only attach up to 8 files.");
            return;
        }
        let item_attachments_ids = [];
        if (item_attachments) {
            console.log(item_attachments);
            for (const item_attachment of item_attachments) {
                var form_data = new FormData()
                form_data.append('file', item_attachment, item_attachment.name)
                const response = await fetch(`${api_url}/attachments`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                    body: form_data
                });
                const response_data = await response.json();
                console.log(response_data)
                item_attachments_ids.push(response_data.id);
            }
        }
        const response = await fetch(`${api_url}/classrooms/${classroom_id}/items`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                type: item_type,
                topic_id: item_topic,
                attachments_id: item_attachments_ids,
                assigned_to_students_id: [],  // TODO: Add students?
                title: item_title,
                description: item_description || null,
                announcement_text: null,
                due_date: item_due_date || null,
                point: item_point || null,
                choices: item_choices.length ? [item_option_1, item_option_2, item_option_3, item_option_4].filter(Boolean) : null,
            })
        });
        is_create_classwork_menu_open = false;
        current_classroom = get_current_classroom();
    }
</script>

<svelte:head>
   <title>Classworks</title>
</svelte:head>

<div class="w-[64rem] mx-auto">
    <nav class="flex">
        <a href="/" class="h-12 w-32 p-3.5 text-center text-gray-600 font-semibold">Home</a>
        <a href="/classrooms/{classroom_id}" class="h-12 w-32 p-3.5 text-center text-gray-600 font-semibold">Stream</a>
        <a href="/classrooms/{classroom_id}/classworks" class="h-12 w-32 p-3.5 text-center text-gray-600 font-semibold border-b-4 border-blue-600">Classwork</a>
        <a href="/classrooms/{classroom_id}/people" class="h-12 w-32 p-3.5 text-center text-gray-600 font-semibold">People</a>
    </nav>
    <hr>
    <div class="flex justify-start ml-16">
        <div class="m-4 flex">
            {#await current_classroom then current_classroom}
                {#await current_user then current_user}
                    {#if current_classroom.owner.id === current_user.id}
                        <button on:click={toggle_create_classwork_menu_state} style="background-color: {current_classroom.theme_color};" class="text-xl text-white p-2.5 pr-5 rounded-full drop-shadow-lg">
                            <span class="material-symbols-outlined relative top-[0.2rem] left-1">
                                add
                            </span>
                            <span class="relative text-base font-medium -top-[0.2rem] ml-2">
                                Create
                            </span>
                        </button>
                    {/if}
                {/await}
            {/await}
        </div>
        <div class="m-4 flex">
            {#await current_classroom then current_classroom}
                {#await current_user then current_user}
                    {#if current_classroom.owner.id === current_user.id}
                        <button on:click={toggle_create_topic_menu_state} style="background-color: {current_classroom.theme_color};" class="text-xl text-white p-2.5 pr-5 rounded-full drop-shadow-lg">
                            <span class="material-symbols-outlined relative top-[0.2rem] left-1">
                                add
                            </span>
                            <span class="relative text-base font-medium -top-[0.2rem] ml-2">
                                Create topic
                            </span>
                        </button>
                    {/if}
                {/await}
            {/await}
        </div>
    </div>
</div>
{#if is_create_classwork_menu_open}
<div transition:fade={{ duration: 150, easing: quadOut }} class="fixed top-0 left-0 bottom-0 right-0 bg-black opacity-50 z-40"></div>
    <div transition:scale={{ duration: 150, easing: quadOut, start: 0.75 }} class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[36rem] h-fit z-50 bg-white rounded-xl p-5">
        <h1 class="text-lg font-medium text-gray-600 inline-block">Create classwork</h1>
        <button class="inline-block cursor-pointer float-right" on:click={() => {is_create_classwork_menu_open = false;}}>
            <span class="material-symbols-outlined">
                close
            </span>
        </button>
        <form on:submit|preventDefault={create_class_item} action="/create_classroom_item" method="post">
            <select 
                class="w-[32rem] h-12 m-auto mt-4 block pl-5 rounded-t-md border-b bg-gray-100 border-solid border-black focus:border-b-2 focus:border-blue-700 outline-none placeholder:text-gray-500"
                bind:value={item_type}
            >
                <option value="Material">Material</option>
                <option value="Assignment">Assignment</option>
            </select>
            <select
                class="w-[32rem] h-12 m-auto mt-4 mb-3 block pl-5 rounded-t-md border-b bg-gray-100 border-solid border-black focus:border-b-2 focus:border-blue-700 outline-none placeholder:text-gray-500"
                bind:value={item_topic}
            >
                {#await current_classroom then current_classroom}
                    <option value="null">No topic</option>
                    {#each current_classroom.topics as topic}
                        <option value={topic.id}>{topic.name}</option>
                    {/each}
                {/await}
            </select>
            <label for="many" class="ml-4">
                Attachments:
            </label>
            <br>
            <input bind:files={item_attachments} id="many" multiple type="file" class="ml-4 mt-1 file:cursor-pointer file:bg-gray-200 file:hover:bg-gray-300 file:mr-2.5 file:border-none file:rounded-lg file:px-2.5 file:py-1" />
            <input
                type="text"
                class="w-[32rem] h-12 m-auto mt-4 block p-5 rounded-t-md border-b bg-gray-100 border-solid border-black focus:border-b-2 focus:border-blue-700 outline-none placeholder:text-gray-500"
                required
                bind:value={item_title}
                placeholder="Title (required)"
            />
            <input
                type="text"
                class="w-[32rem] h-12 m-auto mt-4 block p-5 rounded-t-md border-b bg-gray-100 border-solid border-black focus:border-b-2 focus:border-blue-700 outline-none placeholder:text-gray-500"
                bind:value={item_description}
                placeholder="Description"
            />
            {#if item_type === "Assignment" || item_type === "Question" || item_type === "MultipleChoiceQuestion"}
                <input
                    type="date"
                    class="w-[32rem] h-12 m-auto mt-4 block p-5 rounded-t-md border-b bg-gray-100 border-solid border-black focus:border-b-2 focus:border-blue-700 outline-none placeholder:text-gray-500"
                    bind:value={item_due_date}
                    placeholder="Due date"
                />
                <input
                    type="nubmer"
                    class="w-[32rem] h-12 m-auto mt-4 block p-5 rounded-t-md border-b bg-gray-100 border-solid border-black focus:border-b-2 focus:border-blue-700 outline-none placeholder:text-gray-500"
                    bind:value={item_point}
                    placeholder="Points"
                />
            {/if}
            {#if item_type == "MultipleChoiceQuestion"}
                <input
                    type="text"
                    class="w-[32rem] h-12 m-auto mt-4 block p-5 rounded-t-md border-b bg-gray-100 border-solid border-black focus:border-b-2 focus:border-blue-700 outline-none placeholder:text-gray-500"
                    required
                    bind:value={item_option_1}
                    placeholder="Option 1 (required)"
                />
                <input
                    type="text"
                    class="w-[32rem] h-12 m-auto mt-4 block p-5 rounded-t-md border-b bg-gray-100 border-solid border-black focus:border-b-2 focus:border-blue-700 outline-none placeholder:text-gray-500"
                    required
                    bind:value={item_option_2}
                    placeholder="Option 2 (required)"
                />
                <input
                    type="text"
                    class="w-[32rem] h-12 m-auto mt-4 block p-5 rounded-t-md border-b bg-gray-100 border-solid border-black focus:border-b-2 focus:border-blue-700 outline-none placeholder:text-gray-500"
                    bind:value={item_option_3}
                    placeholder="Option 3"
                />
                <input
                    type="text"
                    class="w-[32rem] h-12 m-auto mt-4 block p-5 rounded-t-md border-b bg-gray-100 border-solid border-black focus:border-b-2 focus:border-blue-700 outline-none placeholder:text-gray-500"
                    bind:value={item_option_4}
                    placeholder="Option 4"
                />
            {/if}
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
{#if is_create_topic_menu_open}
<div transition:fade={{ duration: 150, easing: quadOut }} class="fixed top-0 left-0 bottom-0 right-0 bg-black opacity-50 z-40"></div>
    <div transition:scale={{ duration: 150, easing: quadOut, start: 0.75 }} class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[36rem] h-fit z-50 bg-white rounded-xl p-5">
        <h1 class="text-lg font-medium text-gray-600 inline-block">Create classwork</h1>
        <button class="inline-block cursor-pointer float-right" on:click={() => {is_create_topic_menu_open = false;}}>
            <span class="material-symbols-outlined">
                close
            </span>
        </button>
        <form on:submit|preventDefault={create_topic} action="/create_topic" method="post">
            <input
                type="text"
                class="w-[32rem] h-12 m-auto mt-4 block p-5 rounded-t-md border-b bg-gray-100 border-solid border-black focus:border-b-2 focus:border-blue-700 outline-none placeholder:text-gray-500"
                required
                bind:value={new_topic_name}
                placeholder="Topic name (required)"
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
{#await current_classroom then current_classroom}
    <div class="relative -top-12">
        {#each current_classroom.topics as topic}
            <h1 style="color: {current_classroom.theme_color}; border-color: {current_classroom.theme_color}" class="text-2xl font-medium w-[56rem] mx-auto mt-16 pl-8 pb-4 border-b">{topic.name}</h1>
            {#each current_classroom.items as item}
                {#if item.type !== "Announcement"}
                    {#if item.topic && item.topic.id === topic.id}
                        <a href="/classrooms/{classroom_id}/classworks/{item.id}" class="w-[56rem] mx-auto">
                            <div class="w-[56rem] mx-auto bg-white rounded-lg p-4 border-b border-solid border-gray-300 cursor-pointer hover:drop-shadow-xl">
                                {#if item.type === "Material"}
                                <div style="background-color: {current_classroom.theme_color};" class="h-10 w-10 relative top-1 left-4 text-lg font-semibold text-white rounded-full inline-flex items-center justify-center">
                                    <span class="material-symbols-outlined text-white">
                                        book
                                    </span>
                                </div>
                                {:else if item.type === "Assignment"}
                                <div style="background-color: {current_classroom.theme_color};" class="h-10 w-10 relative top-1 left-4 text-lg font-semibold text-white rounded-full inline-flex items-center justify-center">
                                    <span class="material-symbols-outlined text-white">
                                        assignment
                                    </span>
                                </div>
                                {:else}
                                <div style="background-color: {current_classroom.theme_color};" class="h-10 w-10 relative top-1 left-4 text-lg font-semibold text-white rounded-full inline-flex items-center justify-center">
                                    <span class="material-symbols-outlined text-white">
                                        live_help
                                    </span>
                                </div>
                                {/if}
                                <h1 class="text-lg font-medium ml-7 inline-block text-gray-600">{item.title}</h1>
                            </div>
                        </a>
                    {/if}
                {/if}
            {/each}
        {/each}
        <h1 style="color: {current_classroom.theme_color}; border-color: {current_classroom.theme_color}" class="text-2xl font-medium w-[56rem] mx-auto mt-16 pl-8 pb-4 border-b">No topic</h1>
        {#each current_classroom.items as item}
            {#if item.type !== "Announcement"}
                {#if !item.topic}
                    <a href="/classrooms/{classroom_id}/classworks/{item.id}" class="w-[56rem] mx-auto">
                        <div class="w-[56rem] mx-auto bg-white rounded-lg p-4 border-b border-solid border-gray-300 cursor-pointer hover:drop-shadow-xl">
                            {#if item.type === "Material"}
                            <div style="background-color: {current_classroom.theme_color};" class="h-10 w-10 relative top-1 left-4 text-lg font-semibold text-white rounded-full inline-flex items-center justify-center">
                                <span class="material-symbols-outlined text-white">
                                    book
                                </span>
                            </div>
                            {:else if item.type === "Assignment"}
                            <div style="background-color: {current_classroom.theme_color};" class="h-10 w-10 relative top-1 left-4 text-lg font-semibold text-white rounded-full inline-flex items-center justify-center">
                                <span class="material-symbols-outlined text-white">
                                    assignment
                                </span>
                            </div>
                            {:else}
                            <div style="background-color: {current_classroom.theme_color};" class="h-10 w-10 relative top-1 left-4 text-lg font-semibold text-white rounded-full inline-flex items-center justify-center">
                                <span class="material-symbols-outlined text-white">
                                    live_help
                                </span>
                            </div>
                            {/if}
                            <h1 class="text-lg font-medium ml-7 inline-block text-gray-600">{item.title}</h1>
                        </div>
                    </a>
                {/if}
            {/if}
        {/each}
    </div>
{/await}
