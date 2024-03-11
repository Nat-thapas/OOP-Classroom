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
        <a href="/" class="h-12 w-32 p-3.5 text-center text-gray-600 font-semibold">Home</a>
        <a href="/classrooms/{classroom_id}" class="h-12 w-32 p-3.5 text-center text-gray-600 font-semibold border-b-4 border-blue-600">Stream</a>
        <a href="/classrooms/{classroom_id}/classworks" class="h-12 w-32 p-3.5 text-center text-gray-600 font-semibold">Classwork</a>
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
        <div class="flex">
            <div class="w-44 ml-12 mr-4 mt-4 h-fit">
                {#if current_classroom.code}
                    <div class="p-4 w-44 rounded-lg border border-solid border-gray-300">
                        <h3 class="font-medium">Class code</h3>
                        <p style="color: {current_classroom.theme_color};" class="text-2xl font-semibold">{current_classroom.code}</p>
                    </div>
                {:else}
                <div class="p-4 w-44 rounded-lg border border-solid border-gray-300">
                    <h3 class="font-medium mb-4">Upcoming</h3>
                    <p class="text-gray-500">No work due soon, probably</p>
                </div>
                {/if}
            </div>
            <div class=" w-[44.75rem] m-4 columns-1">
                {#each current_classroom.items as item}
                    {#if item.type === "Announcement"}
                        <h1>Not implemented yet</h1>
                    {:else}
                        <a href="/classrooms/{classroom_id}/classworks/{item.id}" class="w-[56rem] mx-auto">
                            <div class="w-[44rem] h-20 mx-auto bg-white rounded-lg p-4 border border-solid border-gray-300 cursor-pointer hover:drop-shadow-xl">
                                {#if item.type === "Material"}
                                <div style="background-color: {current_classroom.theme_color};" class="h-10 w-10 relative left-2 text-lg font-semibold text-white rounded-full inline-flex items-center justify-center">
                                    <span class="material-symbols-outlined text-white">
                                        book
                                    </span>
                                </div>
                                {:else if item.type === "Assignment"}
                                <div style="background-color: {current_classroom.theme_color};" class="h-10 w-10 relative left-2 text-lg font-semibold text-white rounded-full inline-flex items-center justify-center">
                                    <span class="material-symbols-outlined text-white">
                                        assignment
                                    </span>
                                </div>
                                {:else}
                                <div style="background-color: {current_classroom.theme_color};" class="h-10 w-10 relative left-2 text-lg font-semibold text-white rounded-full inline-flex items-center justify-center">
                                    <span class="material-symbols-outlined text-white">
                                        live_help
                                    </span>
                                </div>
                                {/if}
                                <h1 class="text-base font-medium relative -top-10 left-16 text-gray-600">{item.title}</h1>
                                <h2 class="text-sm relative -top-10 left-16 text-gray-600">Posted: {(new Date(item.created_at)).toDateString()}</h2>
                            </div>
                        </a>
                        <br>
                    {/if}
                {/each}
            </div>
        </div>
    {/await}
</div>
