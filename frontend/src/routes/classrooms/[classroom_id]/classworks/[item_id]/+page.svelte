<script lang="ts">
    export let data;

    const classroom_id: string = data.classroom_id;
    const item_id: string = data.item_id;

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
        return response_data;
    }

    async function get_current_item(): Promise<any> {
        const response = await fetch(`${api_url}/classrooms/${classroom_id}/items/${item_id}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        const response_data = await response.json();
        document.title = "Classwork - " + response_data.title;
        return response_data;
    }

    let current_user: Promise<any> = get_current_user();
    let current_classroom: Promise<any> = get_current_classroom();
    let current_item: Promise<any> = get_current_item();

</script>

<svelte:head>
    <title>Classwork</title>
</svelte:head>

<div class="w-[48rem] mx-auto mt-8">
    {#await current_item then current_item}
        {#await current_classroom then current_classroom}
            <div style="border-color: {current_classroom.theme_color}" class="border-b {current_item.point ? "h-24" : "h-20"}">
                {#if current_item.type === "Material"}
                    <div style="background-color: {current_classroom.theme_color};" class="h-10 w-10 relative top-1 left-4 text-lg font-semibold text-white rounded-full inline-flex items-center justify-center">
                        <span class="material-symbols-outlined text-white">
                            description
                        </span>
                    </div>
                {:else if current_item.type === "Assignment"}
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
                <h1 style="color: {current_classroom.theme_color};" class="text-4xl font-medium m-4 relative -top-14 left-14">{current_item.title}</h1>
                <h2 class="text-gray-500 text-sm relative pl-4 -top-16 left-16">{current_classroom.owner.username} • {(new Date(current_item.created_at)).toDateString()} (Edited {(new Date(current_item.edited_at)).toDateString()})</h2>
                {#if current_item.point}
                    <p class="text-sm m-4 text-gray-700 relative -top-20 left-16">{current_item.point} points</p>
                {/if}
            </div>
            <div class="mt-4">
                {#each current_item.attachments as attachment}
                    <a href={api_url + "/attachments/" + attachment.id + "/data"} target="_blank" class="text-blue-600 underline m-4 block">{attachment.name}</a>
                {/each}
                {#if current_item.description}
                    <p class="m-4 relative -top-20 left-16">{current_item.description}</p>
                {/if}
            </div>
        {/await}
    {/await}
</div>
