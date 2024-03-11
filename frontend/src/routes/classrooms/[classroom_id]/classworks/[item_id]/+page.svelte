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

    async function get_current_submission(): Promise<any> {
        console.log('fetching submission')
        const response = await fetch(`${api_url}/classrooms/${classroom_id}/items/${item_id}/submissions/@me`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        const response_data = await response.json();
        return response_data;
    }

    let current_user: Promise<any> = get_current_user();
    let current_classroom: Promise<any> = get_current_classroom();
    let current_item: Promise<any> = get_current_item();
    let current_submission: Promise<any> = get_current_submission();

    let submission_attachments: FileList;

    async function submit_assignment() {
        let submission_attachments_id = [];
        if (submission_attachments) {
            for (const submission_attachment of submission_attachments) {
                var form_data = new FormData()
                form_data.append('file', submission_attachment, submission_attachment.name)
                const response = await fetch(`${api_url}/attachments`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                    body: form_data
                });
                const response_data = await response.json();
                console.log(response_data)
                submission_attachments_id.push(response_data.id);
            }
        }
        const response = await fetch(`${api_url}/classrooms/${classroom_id}/items/${item_id}/submissions/@me`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                attachments_id: submission_attachments_id,
            })
        });
        const response_data = await response.json();
        current_classroom = get_current_classroom();
        current_item = get_current_item();
        current_submission = get_current_submission();
    }

</script>

<svelte:head>
    <title>Classwork</title>
</svelte:head>

<div class="w-[56rem] mx-auto">
    {#await current_classroom then current_classroom}
    {#await current_user then current_user}
    {#if current_classroom.owner.id === current_user.id}
        <nav class="flex">
            <a href="/classrooms/{classroom_id}/classworks/{item_id}" class="h-12 w-32 p-3.5 text-center text-gray-600 font-semibold border-b-4 border-blue-600">Instructions</a>
            <a href="/classrooms/{classroom_id}/classworks/{item_id}/student-work" class="h-12 w-32 p-3.5 text-center text-gray-600 font-semibold">Student work</a>
        </nav>
        <hr>
    {/if}
    {/await}
    {/await}
    <div class="w-[48rem] mx-auto mt-8">
        {#await current_item then current_item}
            {#await current_classroom then current_classroom}
                <div style="border-color: {current_classroom.theme_color}" class="border-b {current_item.point ? "h-24" : "h-20"}">
                    {#if current_item.type === "Material"}
                        <div style="background-color: {current_classroom.theme_color};" class="h-10 w-10 relative top-1 left-4 text-lg font-semibold text-white rounded-full inline-flex items-center justify-center">
                            <span class="material-symbols-outlined text-white">
                                book
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
                    {#if current_item.due_date}
                        <p class="text-sm m-4 text-gray-700 relative -top-24 left-[36rem]">Due: {(new Date(current_item.due_date)).toDateString()}</p>
                    {/if}
                </div>
                <div class="flex w-[64rem] ml-16">
                    <div class="mt-4 w-[28rem]">
                        <p class="m-4 relative text-gray-600">{current_item.description || "No description"}</p>
                        {#each current_item.attachments as attachment}
                            <a href={api_url + "/attachments/" + attachment.id + "/data"} target="_blank" class="text-blue-600 underline m-4 block relative">{attachment.name}</a>
                        {/each}
                    </div>
                    {#await current_user then current_user}
                        {#if current_item.type === "Assignment" && current_user.id !== current_classroom.owner.id}
                            <div class="w-56 m-4 rounded-lg border border-gray-300 bg-white drop-shadow-lg p-4">
                                <h3 class="text-2xl text-gray-700">Your work</h3>
                                {#await current_submission then current_submission}
                                    {#if current_submission.point}
                                        <p>Graded: {current_submission.point}/{current_item.point || 0}</p>
                                    {/if}
                                    {#if current_submission.attachments && current_submission.attachments.length > 0}
                                        {#each current_submission.attachments as attachment}
                                            <a href={api_url + "/attachments/" + attachment.id + "/data"} target="_blank" class="text-blue-600 underline m-4 block relative">{attachment.name}</a>
                                        {/each}
                                    {/if}
                                    <input bind:files={submission_attachments} id="many" multiple type="file" class="mt-4 ml-10 file:cursor-pointer file:bg-gray-200 file:hover:bg-gray-300 file:mr-2.5 file:mb-2 file:border-none file:rounded-lg file:px-2.5 file:py-1 file:block" />
                                    {#if current_submission.attachments && current_submission.attachments.length > 0}
                                        <button on:click={submit_assignment} style="background-color: {current_classroom.theme_color};" class="px-4 py-2 rounded-lg text-white w-44 ml-2 mt-4">Resubmit</button>
                                    {:else}
                                        <button on:click={submit_assignment} style="background-color: {current_classroom.theme_color};" class="px-4 py-2 rounded-lg text-white w-44 ml-2 mt-4">{submission_attachments && submission_attachments.length > 0 ? "Submit" : "Mark as done"}</button>
                                    {/if}
                                {/await}
                            </div>
                        {/if}
                    {/await}
                </div>
            {/await}
        {/await}
    </div>
</div>

