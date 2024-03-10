<script lang="ts">
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
        document.title = "Classroom - " + response_data.name;
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
        <a href="/classrooms/{classroom_id}" class="h-12 w-32 p-3.5 text-center text-gray-600 font-semibold border-b-4 border-blue-600">Stream</a>
        <a href="/classrooms/{classroom_id}/classwork" class="h-12 w-32 p-3.5 text-center text-gray-600 font-semibold">Classwork</a>
        <a href="/classrooms/{classroom_id}/people" class="h-12 w-32 p-3.5 text-center text-gray-600 font-semibold">People</a>
    </nav>
    <hr>
    {#await current_classroom then current_classroom}
        <div style="background-image: url({api_url}/{current_classroom.banner_path}); background-repeat: no-repeat; background-size: contain;" class="w-[58rem] h-[14.5rem] rounded-xl m-12 mb-0">
            {#if current_classroom.section}
                <h1 class="relative top-36 left-7 text-4xl text-white font-medium">{current_classroom.name}</h1>
                <h2 class="relative top-36 left-7 text-2xl text-white font-semibold">{current_classroom.section}</h2>
            {:else}
                <h1 class="relative top-40 left-7 text-4xl text-white font-semibold">{current_classroom.name}</h1>
            {/if}
        </div>
        {#await current_user then current_user}
            {#if current_classroom.owner.id === current_user.id}
                <div class="flex mx-12 mt-4">
                    <div class="p-4 w-44 rounded-lg border border-solid border-gray-300">
                        <h3 class="font-medium">Class code</h3>
                        <p style="color: {current_classroom.theme_color};" class="text-2xl font-semibold">{current_classroom.code}</p>
                    </div>
                </div>
            {/if}
        {/await}
    {/await}
</div>
