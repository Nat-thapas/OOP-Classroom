<script lang="ts">
    import { onMount } from 'svelte';
    import { fade, scale } from 'svelte/transition';
    import { quadOut } from 'svelte/easing';

    export let data;

    const classroom_id: string = data.classroom_id;

    const api_url: string = import.meta.env.VITE_API_URL;

	const token: string | null = localStorage.getItem('token');

    const theme_colors: string[] = ["#1967d2","#1e8e3e","#e52592","#e8710a","#129eaf","#9334e6","#4285f4","#5f6368"];

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
    
    async function get_banners_path(): Promise<any> {
        const response = await fetch(`${api_url}/classrooms/banner-images`, {
            method: 'GET',
        });
        const response_data = await response.json();
        return response_data;
    }

    async function get_current_tasks(): Promise<any> {
        const response = await fetch(`${api_url}/tasks/@me?task_type=ToDo`, {
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
    let banners_path: Promise<any> = get_banners_path();
    let current_tasks: Promise<any> = get_current_tasks();

    let is_edit_classroom_menu_open: boolean = false;
    let is_customize_classroom_menu_open: boolean = false;
    let is_select_banner_menu_open: boolean = false;

    function toggle_edit_classroom_menu_state() {
        is_edit_classroom_menu_open = !is_edit_classroom_menu_open;
    }

    function toggle_customize_classroom_menu_state() {
        is_customize_classroom_menu_open = !is_customize_classroom_menu_open;
    }

    function toggle_select_banner_menu_state() {
        is_select_banner_menu_open = !is_select_banner_menu_open;
    }

    let edit_classroom_name: string = "";
    let edit_classroom_section: string = "";
    let edit_classroom_subject: string = "";
    let edit_classroom_room: string = "";
    let edit_classroom_banner_path: string = "";
    let edit_classroom_theme_color: string = "";

    async function edit_classroom() {
        if (edit_classroom_name.length > 48) {
            alert("Classname must be less than 48 characters long");
            return;
        }
        if (edit_classroom_section && edit_classroom_section.length > 16) {
            alert("Section must be less than 16 characters long");
            return;
        }
        if (edit_classroom_subject && edit_classroom_subject.length > 32) {
            alert("Subject must be less than 32 characters long");
            return;
        }
        if (edit_classroom_room && edit_classroom_room.length > 16) {
            alert("Room must be less than 16 characters long");
            return;
        }
        const response = await fetch(`${api_url}/classrooms/${classroom_id}`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: edit_classroom_name,
                section: edit_classroom_section || null,
                subject: edit_classroom_subject || null,
                room: edit_classroom_room || null,
                banner_path: edit_classroom_banner_path,
                theme_color: edit_classroom_theme_color,
            })
        });
        const response_data = await response.json();
        current_classroom = get_current_classroom();
        is_edit_classroom_menu_open = false;
        alert("Classsroom edited successfully");
    }

    async function customize_classroom() {
        const response = await fetch(`${api_url}/classrooms/${classroom_id}`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: edit_classroom_name,
                section: edit_classroom_section || null,
                subject: edit_classroom_subject || null,
                room: edit_classroom_room || null,
                banner_path: edit_classroom_banner_path,
                theme_color: edit_classroom_theme_color,
            })
        });
        const response_data = await response.json();
        current_classroom = get_current_classroom();
        is_edit_classroom_menu_open = false;
        alert("Classsroom customized successfully");
        const classroom = await current_classroom;
        document.title = "Classroom - " + classroom.name;
        edit_classroom_name = classroom.name;
        edit_classroom_section = classroom.section;
        edit_classroom_subject = classroom.subject;
        edit_classroom_room = classroom.room;
        edit_classroom_banner_path = classroom.banner_path;
        edit_classroom_theme_color = classroom.theme_color;
    }

    async function set_classroom_theme_color(evnt: Event) {
        const response = await fetch(`${api_url}/classrooms/${classroom_id}`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: edit_classroom_name,
                section: edit_classroom_section || null,
                subject: edit_classroom_subject || null,
                room: edit_classroom_room || null,
                banner_path: edit_classroom_banner_path,
                theme_color: evnt.target.dataset.color,
            })
        });
        const response_data = await response.json();
        current_classroom = get_current_classroom();
        is_edit_classroom_menu_open = false;
        const classroom = await current_classroom;
        document.title = "Classroom - " + classroom.name;
        edit_classroom_name = classroom.name;
        edit_classroom_section = classroom.section;
        edit_classroom_subject = classroom.subject;
        edit_classroom_room = classroom.room;
        edit_classroom_banner_path = classroom.banner_path;
        edit_classroom_theme_color = classroom.theme_color;
    }

    async function set_banner_image(evnt: Event) {
        console.log(evnt.target)
        const response = await fetch(`${api_url}/classrooms/${classroom_id}`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: edit_classroom_name,
                section: edit_classroom_section || null,
                subject: edit_classroom_subject || null,
                room: edit_classroom_room || null,
                banner_path: evnt.target.dataset.bannerpath,
                theme_color: edit_classroom_theme_color,
            })
        });
        const response_data = await response.json();
        current_classroom = get_current_classroom();
        is_edit_classroom_menu_open = false;
        is_select_banner_menu_open = false;
        const classroom = await current_classroom;
        document.title = "Classroom - " + classroom.name;
        edit_classroom_name = classroom.name;
        edit_classroom_section = classroom.section;
        edit_classroom_subject = classroom.subject;
        edit_classroom_room = classroom.room;
        edit_classroom_banner_path = classroom.banner_path;
        edit_classroom_theme_color = classroom.theme_color;
    }

    let announcement_attachments: FileList;
    let announcement_text: string;

    async function create_announcement() {
        let announcement_attachments_id = [];
        if (announcement_attachments) {
            for (const announcement_attachment of announcement_attachments) {
                var form_data = new FormData()
                form_data.append('file', announcement_attachment, announcement_attachment.name)
                const response = await fetch(`${api_url}/attachments`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                    body: form_data
                });
                const response_data = await response.json();
                console.log(response_data)
                announcement_attachments_id.push(response_data.id);
            }
        }
        const response = await fetch(`${api_url}/classrooms/${classroom_id}/items`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                type: "Announcement",
                topic_id: null,
                attachments_id: announcement_attachments_id,
                assigned_to_students_id: [],  // TODO: Add students?
                title: null,
                description: null,
                announcement_text: announcement_text,
                due_date: null,
                point: null,
                choices: null,
            })
        });
        const response_data = await response.json();
        current_classroom = get_current_classroom();
        announcement_text = "";
        alert("Announcement created successfully")
    }

    let comment_text: string;

    async function add_class_comment(evnt: Event) {
        console.log(evnt.target)
        const response = await fetch(`${api_url}/classrooms/${classroom_id}/items/${evnt.target.dataset.announcementid}/comments`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                comment: comment_text
            })
        });
        const response_data = await response.json();
        current_classroom = get_current_classroom();
        comment_text = "";
    }

    async function delete_classroom() {
        let user_response = prompt("Are you sure you want to delete this classroom? Type 'DELETE' to confirm");
        if (!user_response) {
            return;
        }
        user_response = user_response.trim();
        user_response = user_response.toUpperCase();
        if (user_response !== "DELETE") {
            return;
        }
        const response = await fetch(`${api_url}/classrooms/${classroom_id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`,
            }
        });
        window.location.href = "/";
    }

    onMount(async () => {
        const classroom = await current_classroom;
        document.title = "Classroom - " + classroom.name;
        edit_classroom_name = classroom.name;
        edit_classroom_section = classroom.section;
        edit_classroom_subject = classroom.subject;
        edit_classroom_room = classroom.room;
        edit_classroom_banner_path = classroom.banner_path;
        edit_classroom_theme_color = classroom.theme_color;
    });
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
                    <button on:click={toggle_edit_classroom_menu_state} style="background-color: {current_classroom.theme_color};" class="p-2 w-44 mt-4 rounded-lg text-white text-xl">
                        <div class="flex items-center ml-10">
                            <span class="material-symbols-outlined mr-4">
                                edit_square
                            </span>
                            Edit
                        </div>
                    </button>
                    <button on:click={toggle_customize_classroom_menu_state} style="background-color: {current_classroom.theme_color};" class="p-2 w-44 mt-4 rounded-lg text-white text-xl">
                        <div class="flex items-center ml-3">
                            <span class="material-symbols-outlined mr-3">
                                edit
                            </span>
                            Customize
                        </div>
                    </button>
                    <button on:click={delete_classroom} style="background-color: {current_classroom.theme_color};" class="p-2 w-44 mt-4 rounded-lg text-white text-xl">
                        <div class="flex items-center ml-7">
                            <span class="material-symbols-outlined mr-3">
                                delete
                            </span>
                            Delete
                        </div>
                    </button>
                {:else}
                <div class="p-4 w-44 rounded-lg border border-solid border-gray-300">
                    <h3 class="font-medium mb-4">Upcoming</h3>
                    {#await current_tasks then current_tasks}
                        {#if current_tasks.length === 0}
                            <p class="text-gray-600">No upcoming tasks</p>
                        {:else}
                            {#each current_tasks as task}
                                <a href="/classrooms/{classroom_id}/classworks/{task.item_id}" class="underline text-gray-600 block mb-2">{task.title}</a>
                            {/each}
                        {/if}
                    {/await}
                </div>
                {/if}
            </div>
            <div class=" w-[44.75rem] m-4 columns-1">
                {#await current_user then current_user}
                    {#if current_user.id == current_classroom.owner.id}
                        <div class="w-[44rem] h-48 mx-auto mb-6 bg-white rounded-lg p-4 border border-solid border-gray-300 hover:drop-shadow-xl">
                            <h2 class="text-gray-600">Create announcement</h2>
                            <textarea bind:value={announcement_text} class="mt-3 w-[42rem] p-2 resize-none rounded-lg border border-gray-300"></textarea>
                            <button on:click={create_announcement} style="background-color: {current_classroom.theme_color};" class="text-white px-4 py-2 rounded-lg mt-3 w-80">Create</button>
                            <input bind:files={announcement_attachments} id="many" multiple type="file" class="mt-4 ml-10 file:cursor-pointer file:bg-gray-200 file:hover:bg-gray-300 file:mr-2.5 file:mb-2 file:border-none file:rounded-lg file:px-2.5 file:py-1" />
                        </div>
                    {/if}
                {/await}
                {#each current_classroom.items as item (item.id)}
                    {#if item.type === "Announcement"}
                        <div class="w-[44rem] h-fit mx-auto mb-6 bg-white rounded-lg p-4 border border-solid border-gray-300 hover:drop-shadow-xl">
                            <img src="{api_url}/users/{current_classroom.owner.id}/avatar/data" alt="Avatar" class="w-10 h-10 relative left-2 rounded-full">
                            <h1 class="text-base font-medium relative -top-10 left-16 text-gray-600">{current_classroom.owner.username}</h1>
                            <h2 class="text-sm relative -top-10 left-16 text-gray-600">Posted: {(new Date(item.created_at)).toDateString()}</h2>
                            <p class="border-t border-gray-300 w-[42rem] text-wrap break-words relative -top-4 pt-4">{item.announcement_text}</p>
                            {#if item.attachments}
                                {#each item.attachments as attachment (attachment.id)}
                                    <a href={api_url + "/attachments/" + attachment.id + "/data"} target="_blank" class="text-blue-600 underline m-4 block">{attachment.name}</a>
                                {/each}
                            {/if}
                            {#if item.comments && item.comments.length > 0}
                                <h4 class="text-xl border-t pt-4 border-gray-300">Class comments</h4>
                                {#each item.comments as comment}
                                    <div class="flex items-center m-4">
                                        <img src="{api_url}/users/{comment.owner.id}/avatar/data" alt="Profile" class="w-8 h-8 rounded-full " />
                                        <div>
                                            <div class="flex items-center">
                                                <p class="text-gray-600 ml-4 font-medium">{comment.owner.username}</p>
                                                <p class="ml-4 text-gray-500">{(new Date(comment.created_at)).toDateString()}</p>
                                            </div>
                                            <p class="text-gray-600 ml-4 block">{comment.text}</p>
                                        </div>
                                    </div>
                                {/each}
                            {/if}
                            {#await current_user then current_user}
                                <div class="w-[42rem] pt-4 border-t border-gray-300">
                                    <div class="flex items-center">
                                        <img src="{api_url}/users/{current_user.id}/avatar/data" alt="Profile" class="w-8 h-8 rounded-full " />
                                        <input bind:value={comment_text} type="text" class="w-[40rem] border border-gray-300 rounded-lg p-2.5 ml-4" placeholder="Add class comment" />
                                        <button on:click={add_class_comment} data-announcementid={item.id} class="relative -left-8 top-1">
                                            <span class="material-symbols-outlined text-gray-500" data-announcementid={item.id}>
                                                send
                                            </span>
                                        </button>
                                    </div>
                                </div>
                            {/await}
                        </div>
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
{#if is_edit_classroom_menu_open}
    <div transition:fade={{ duration: 150, easing: quadOut }} class="fixed top-0 left-0 bottom-0 right-0 bg-black opacity-50 z-40"></div>
    <div transition:scale={{ duration: 150, easing: quadOut, start: 0.75 }} class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[36rem] h-fit z-50 bg-white rounded-xl p-5">
        <h1 class="text-lg font-medium text-gray-600 inline-block">Edit class</h1>
        <button class="inline-block cursor-pointer float-right" on:click={() => {is_edit_classroom_menu_open = false;}}>
            <span class="material-symbols-outlined">
                close
            </span>
        </button>
        <form on:submit|preventDefault={edit_classroom} action="/edit_classroom" method="post">
            <input
                type="text"
                class="w-[32rem] h-12 m-auto mt-4 block p-5 rounded-t-md border-b bg-gray-100 border-solid border-black focus:border-b-2 focus:border-blue-700 outline-none placeholder:text-gray-500"
                required
                placeholder="Classname (required)"
                bind:value={edit_classroom_name}
            />
            <input
                type="text"
                class="w-[32rem] h-12 m-auto mt-4 block p-5 rounded-t-md border-b bg-gray-100 border-solid border-black focus:border-b-2 focus:border-blue-700 outline-none placeholder:text-gray-500"
                placeholder="Section"
                bind:value={edit_classroom_section}
            />
            <input
                type="text"
                class="w-[32rem] h-12 m-auto mt-4 block p-5 rounded-t-md border-b bg-gray-100 border-solid border-black focus:border-b-2 focus:border-blue-700 outline-none placeholder:text-gray-500"
                placeholder="Subject"
                bind:value={edit_classroom_subject}
            />
            <input
                type="text"
                class="w-[32rem] h-12 m-auto mt-4 mb-8 block p-5 rounded-t-md border-b bg-gray-100 border-solid border-black focus:border-b-2 focus:border-blue-700 outline-none placeholder:text-gray-500"
                placeholder="Room"
                bind:value={edit_classroom_room}
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
{#if is_customize_classroom_menu_open}
    <div transition:fade={{ duration: 150, easing: quadOut }} class="fixed top-0 left-0 bottom-0 right-0 bg-black opacity-50 z-40"></div>
    <div transition:scale={{ duration: 150, easing: quadOut, start: 0.75 }} class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[36rem] h-fit z-50 bg-white rounded-xl p-5">
        <h1 class="text-lg font-medium text-gray-600 inline-block">Customize appearance</h1>
        <button class="inline-block cursor-pointer float-right" on:click={() => {is_customize_classroom_menu_open = false;}}>
            <span class="material-symbols-outlined">
                close
            </span>
        </button>
        {#await current_classroom then current_classroom}
            <div style="background-image: url({api_url}/{current_classroom.banner_path}); background-repeat: no-repeat; background-size: contain;" class="w-[32rem] h-[8rem] rounded-xl ml-2 mt-4"></div>
            <div class="flex items-center">
                <h4 class="text-gray-600 ml-2 mt-4 block">Select banner image</h4>
                <button on:click={toggle_select_banner_menu_state} class="flex items-center relative left-[13.5rem] top-2 px-4 py-2 rounded-xl bg-gray-100 hover:bg-gray-200">
                    <span class="material-symbols-outlined inline-block mr-2">
                        image
                    </span>
                    Select photo
                </button>
            </div>
            <div class="mt-4">
                <h4 class="text-gray-600 ml-2 mt-4 block">Select theme color</h4>
                <div class="flex items-center">
                    {#each theme_colors as theme_color, index}
                        <button on:click={set_classroom_theme_color} data-color="{theme_color}" style="background-color: {theme_color};" class="h-12 w-12 mt-4 mr-4 text-lg font-semibold text-white rounded-full inline-flex items-center justify-center {index === 0 ? "ml-4" : ""}">
                            {#if current_classroom.theme_color == theme_color}
                            <span class="material-symbols-outlined text-white text-3xl">
                                done
                            </span>
                            {/if}
                        </button>
                    {/each}
                </div>
            </div>
        {/await}
    </div>
{/if}
{#if is_select_banner_menu_open}
    <div transition:fade={{ duration: 150, easing: quadOut }} class="fixed top-0 left-0 bottom-0 right-0 bg-black opacity-50 z-40"></div>
    <div transition:scale={{ duration: 150, easing: quadOut, start: 0.75 }} class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[36rem] h-fit z-50 bg-white rounded-xl p-5">
        <h1 class="text-lg font-medium text-gray-600 inline-block">Select banner</h1>
        <button class="inline-block cursor-pointer float-right" on:click={() => {is_select_banner_menu_open = false;}}>
            <span class="material-symbols-outlined">
                close
            </span>
        </button>
        {#await banners_path then banners_path}
            {#each Object.entries(banners_path) as [banner_category, banners_name]}
                {#if banner_category == "General"}
                    <div class="flex flex-wrap w-[32rem] ml-6">
                        {#each banners_name as banner_name}
                            <button on:click={set_banner_image} data-bannerpath="static/banner-images/{banner_category}/{banner_name}">
                                <img src="{api_url}/static/banner-images/{banner_category}/{banner_name}" data-bannerpath="static/banner-images/{banner_category}/{banner_name}" alt="Banner" class="w-56 rounded-md m-2">
                            </button>
                        {/each}
                    </div>
                {/if}
            {/each}
        {/await}
    </div>
{/if}
