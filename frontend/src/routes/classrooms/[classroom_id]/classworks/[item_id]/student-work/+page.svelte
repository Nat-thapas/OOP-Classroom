<script lang="ts">
    import { fade, scale } from 'svelte/transition';
    import { quadOut } from 'svelte/easing';
	import { onMount } from 'svelte';

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

    async function get_current_submissions(): Promise<any> {
        const response = await fetch(`${api_url}/classrooms/${classroom_id}/items/${item_id}/submissions`, {
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
    let current_submissions: Promise<any> = get_current_submissions();

    let grades: number[] = [];

    onMount(async () => {
        const user = await current_user;
        const classroom = await current_classroom;
        if (user.id !== classroom.owner.id) {
            window.location.href = `/classrooms/${classroom_id}/classworks/${item_id}`;
        }

        const submissions = await current_submissions;

        for (let i = 0; i < submissions.length; i++) {
            grades.push(submissions[i].point);
        }
    });

    async function save_grades() {
        const submissions = await current_submissions;
        if (grades.length !== submissions.length) {
            alert('Grade and submission lenght does not match');
            return;
        }
        for (let i = 0; i < submissions.length; i++) {
            const grade = grades[i];
            if (grade < 0) {
                alert('Grade cannot be negative, skipping this submission');
                continue;
            }
            const response = await fetch(`${api_url}/classrooms/${classroom_id}/items/${item_id}/submissions/${submissions[i].id}`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    point: grades[i]
                })
            });
            const response_data = await response.json();
        }
        alert('Grades updated successfully')
    }
</script>

<svelte:head>
   <title>Classroom</title>
</svelte:head>

<div class="w-[56rem] mx-auto">
    <nav class="flex">
        <a href="/classrooms/{classroom_id}/classworks/{item_id}" class="h-12 w-32 p-3.5 text-center text-gray-600 font-semibold">Instructions</a>
        <a href="/classrooms/{classroom_id}/classworks/{item_id}/student-work" class="h-12 w-32 p-3.5 text-center text-gray-600 font-semibold border-b-4 border-blue-600">Student work</a>
    </nav>
    <hr>
    <div class="w=[52rem] mx-8 mt-8">
        {#await current_item then current_item}
            {#await current_submissions then current_submissions}
                {#each current_submissions as submission, index}
                    <div class="flex items-center">
                        <img src="{api_url}/users/{submission.owner.id}/avatar/data" alt="Profile" class="w-8 h-8 rounded-full " />
                        <h1 class="text-gray-600 ml-2.5 w-24">{submission.owner.username}</h1>
                        <input bind:value={grades[index]} type="number" placeholder="___" class="w-10">
                        <p>/{current_item.point || 0}</p>
                        {#each submission.attachments as attachment}
                            <a href={api_url + "/attachments/" + attachment.id + "/data"} target="_blank" class="text-blue-600 underline m-4 block relative">{attachment.name}</a>
                        {/each}
                    </div>
                {/each}
            {/await}
        {/await}
        {#await current_classroom then current_classroom}
            <button on:click={save_grades} style="background-color: {current_classroom.theme_color};" class="text-white text-xl rounded-lg px-12 py-2 mt-8">Save</button>
        {/await}
    </div>
</div>