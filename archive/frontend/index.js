const apiURL = "http://127.0.0.1:8080";

const classroomsDiv = document.getElementById("classrooms");
const addClassroomButton = document.getElementById("add-classroom-button");

async function checkToken(token) {
    const response = await fetch(`${apiURL}/verify?token=${token}`);
    console.log("Token verification endpoint responded with");
    console.log(response);
    return response.status == 200;
}

async function getClasssrooms(token) {
    const response = await fetch(`${apiURL}/classrooms?token=${token}`)
    console.log("Get classrooms endpoint responded with");
    console.log(response);
    const classrooms = await response.json();
    console.log("Got the following classrooms");
    console.log(classrooms)
    return classrooms.classrooms_data;
}

async function main() {
    const token = localStorage.getItem("token");
    const tokenIsValid = await checkToken(token);
    if (!tokenIsValid) {
        console.log("Invalid token, redirecting to login page");
        window.location.replace("/login.html");
        return;
    }
    const classrooms = await getClasssrooms(token);
    classrooms.forEach(classroom => {
        console.log("Adding classroom: ");
        console.log(classroom);
        let classroomDiv = document.createElement("div");
        classroomDiv.id = classroom.id;
        classroomDiv.className = "classroom";
        let classroomNameSpan = document.createElement("span");
        classroomNameSpan.className = "classroom-name";
        let classroomSectionSpan = document.createElement("span");
        classroomSectionSpan.className = "classroom-section";
        let classroomOwnerSpan = document.createElement("span");
        classroomOwnerSpan.className = "classroom-owner";
        classroomNameSpan.innerHTML = classroom.name;
        classroomSectionSpan.innerHTML = "Section: " +  classroom.section;
        classroomOwnerSpan.innerHTML = "Owner: " +  classroom.owner_name;
        classroomDiv.appendChild(classroomNameSpan);
        classroomDiv.appendChild(classroomSectionSpan);
        classroomDiv.appendChild(classroomOwnerSpan);
        if (classroom.code) {
            let classroomCodeSpan = document.createElement("span");
            classroomCodeSpan.className = "classroom-code-display";
            classroomCodeSpan.innerHTML = "Code: " + classroom.code;
            classroomDiv.appendChild(classroomCodeSpan);
        }
        classroomDiv.addEventListener('click', function() {
            localStorage.setItem("currentClassroom", classroom.id);
            location.href = "/classroom.html";
        }, false);
        classroomsDiv.appendChild(classroomDiv);
    });
}

async function joinOrCreateClass() {
    const code = document.getElementById("classroom-code").value;
    const token = localStorage.getItem("token");
    if (code) {
        const response = await fetch(`${apiURL}/join-classroom`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token: token,
                code: code
            }),
        });
        if (response.status != 200) {
            alert("Cannot join class, please check the classroom code");
            return;
        } else {
            location.reload();
            return;
        }
    } else {
        window.location.href = "/create-classroom.html"
    }
}

addClassroomButton.addEventListener("click", joinOrCreateClass);

main();