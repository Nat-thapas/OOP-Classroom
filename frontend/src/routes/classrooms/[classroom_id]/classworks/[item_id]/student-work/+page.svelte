<script lang="ts">
    import { fade, scale } from 'svelte/transition';
    import { quadOut } from 'svelte/easing';

    export let data;

    const classroom_id: string = data.classroom_id;
    const item_id: string = data.item_id;

    const api_url: string = import.meta.env.VITE_API_URL;

	const token: string | null = localStorage.getItem('token');
</script>

<svelte:head>
   <title>Classroom</title>
</svelte:head>

<div class="w-[56rem] mx-auto">
    <nav class="flex">
        <a href="/classrooms/{classroom_id}/classworks/{item_id}" class="h-12 w-32 p-3.5 text-center text-gray-600 font-semibold">Instructions</a>
            <a href="/classrooms/{classroom_id}/classworks/{item_id}/student-work" class="h-12 w-32 p-3.5 text-center text-gray-600 font-semibold border-b-4 border-blue-600">Student work</a>
    </nav>
</div>