const apiURL = "http://127.0.0.1:8080";

const createClassroomForm = document.getElementById("create-classroom-form")

async function processCreateClassroomForm(evnt) {
    console.log("Form submit event received");
    evnt.preventDefault();
    let data = new FormData(evnt.target);
    console.log("Form contain the following data");
    console.log(data);
    console.log(`POSTing name: ${data.get("name")}, subject: ${data.get("subject")}, section: ${data.get("section")}, room: ${data.get("room")}`);
    const token = localStorage.getItem("token");
    const response = await fetch(`${apiURL}/create-classroom`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            token: token,
            name: data.get("name"),
            subject: data.get("subject"),
            section: data.get("section"),
            room: data.get("room"),
        }),
    });
    if (response.status != 200) {
        alert("Invalid information, maybe that classroom already exist?");
        return;
    }
    window.location.href = "/";
}

createClassroomForm.addEventListener("submit", processCreateClassroomForm);