const apiURL = "http://127.0.0.1:8080";

const register_form = document.getElementById("register-form")

async function processRegisterForm(evnt) {
    console.log("Form submit event received");
    evnt.preventDefault();
    let data = new FormData(evnt.target);
    console.log("Form contain the following data");
    console.log(data);
    console.log(`POSTing name: ${data.get("name")}, email: ${data.get("email")}, password: ${data.get("password")}`);
    const response = await fetch(`${apiURL}/register`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: data.get("name"),
            email: data.get("email"),
            password: data.get("password")
        }),
    });
    if (response.status != 200) {
        alert("Invalid information, maybe you already have an account?");
        return;
    }
    const responseData = await response.json();
    const token = responseData.token;
    localStorage.setItem("token", token);
    window.location.href = "/";
}

register_form.addEventListener("submit", processRegisterForm);