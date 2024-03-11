<script lang="ts">
    import { onMount } from 'svelte';
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
        document.title = "People - " + response_data.name;
        return response_data;
    }

    let current_user: Promise<any> = get_current_user();
    let current_classroom: Promise<any> = get_current_classroom();

</script>

<svelte:head>
    <title>Classroom</title>
</svelte:head>

<div class="w-[64rem] mx-auto">
    <nav class="flex">
        <a href="/" class="h-12 w-32 p-3.5 text-center text-gray-600 font-semibold">Home</a>
        <a href="/classrooms/{classroom_id}" class="h-12 w-32 p-3.5 text-center text-gray-600 font-semibold">Stream</a>
        <a href="/classrooms/{classroom_id}/classworks" class="h-12 w-32 p-3.5 text-center text-gray-600 font-semibold">Classwork</a>
        <a href="/classrooms/{classroom_id}/people" class="h-12 w-32 p-3.5 text-center text-gray-600 font-semibold border-b-4 border-blue-600">People</a>
    </nav>
    <hr>
    {#await current_classroom then current_classroom}
        <div class="w-[48rem] mx-auto mt-8">
            <h1 style="color: {current_classroom.theme_color}; border-color: {current_classroom.theme_color};" class="text-3xl w-[48rem] border-b pb-4 mb-4">Teacher</h1>
            <div class="flex items-center ml-4">
                <img src="{api_url}/users/{current_classroom.owner.id}/avatar/data" alt="Profile" class="w-8 h-8 rounded-full" />
                <p class="text-gray-600 ml-4 font-medium">{current_classroom.owner.username}</p>
            </div>
            <h1 style="color: {current_classroom.theme_color}; border-color: {current_classroom.theme_color};" class="text-3xl w-[48rem] border-b pb-4 mb-4 mt-12">Classmates</h1>
            {#each current_classroom.students as student}
                <div class="flex items-center ml-4 pb-3 mb-3 border-b border-gray-300">
                    <img src="{api_url}/users/{student.id}/avatar/data" alt="Profile" class="w-8 h-8 rounded-full" />
                    <p class="text-gray-600 ml-4 font-medium">{student.username}</p>
                </div>
            {/each}
        </div>
    {/await}
</div>
