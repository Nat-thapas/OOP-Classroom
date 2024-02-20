const apiURL = "http://127.0.0.1:8080";

const loginForm = document.getElementById("login-form")

async function processLoginForm(evnt) {
    console.log("Form submit event recieved");
    evnt.preventDefault();
    const data = new FormData(evnt.target);
    console.log(`POSTing email: ${data.get("email")}, password: ${data.get("password")}`);
    const response = await fetch(`${apiURL}/login`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: data.get("email"),
            password: data.get("password")
        }),
    });
    if (response.status != 200) {
        alert("Invalid credential");
        return;
    }
    const responseData = await response.json();
    const token = responseData.token;
    localStorage.setItem("token", token);
    window.location.href = "/";
}

loginForm.addEventListener("submit", processLoginForm);