<script lang="ts">
	const api_url: string = import.meta.env.VITE_API_URL;

	let username: string;
	let email: string;
	let password: string;

	async function register() {
        if (username.length < 3 || username.length > 64) {
            alert('Username must be between 3 and 64 characters long');
            return;
        }
		if (password.length < 8 || password.length > 64) {
			alert('Password must be between 8 and 64 characters long');
			return;
		}
		const response = await fetch(`${api_url}/auth/register`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ username, email, password })
		});
		const response_data = await response.json();
		if (response.status !== 201) {
            if (response.status !== 422) {
                alert(response_data.detail);
                return;
            }
            alert("Failed to register");
            return;
        }
		const token: string = response_data.access_token;
		localStorage.setItem('token', token);
		window.location.href = '/';
	}
</script>

<svelte:head>
	<title>Classroom - Register</title>
</svelte:head>

<div class="w-96 h-fit m-auto mt-36 rounded-lg border border-solid border-gray-300">
	<h1 class="text-3xl mt-8 text-center">Register</h1>
	<form on:submit|preventDefault={register} action="/register" method="post">
		<input
			type="text"
			class="w-80 h-10 m-auto mt-8 block p-5 rounded-lg border border-solid border-gray-300"
			required
			placeholder="Username"
			bind:value={username}
		/>
		<input
			type="email"
			class="w-80 h-10 m-auto mt-4 block p-5 rounded-lg border border-solid border-gray-300"
			required
			placeholder="Email"
			bind:value={email}
		/>
		<input
			type="password"
			class="w-80 h-10 m-auto mt-4 block p-5 rounded-lg border border-solid border-gray-300"
			required
			placeholder="Password"
			bind:value={password}
		/>
		<a href="/login" class="w-80 h-10 m-auto mt-4 block text-blue-500 text-center"
			>Already have an account? Login</a
		>
		<button
			type="submit"
			class="w-80 h-10 m-auto mt-4 block bg-blue-500 text-white rounded-full mb-8 hover:bg-blue-600 hover:drop-shadow-md duration-100 ease-in"
			>Register</button
		>
	</form>
</div>
