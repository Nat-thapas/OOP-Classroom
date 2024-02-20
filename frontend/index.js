const apiURL = "http://127.0.0.1:8080";

const classroomsDiv = document.getElementById("classrooms");

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
        console.log("Adding classroom: ")
        console.log(classroom);
        let classroomDiv = document.createElement("div");
        classroomDiv.id = classroom.id;
        classroomDiv.className = "classroom";
        classroomDiv.innerHTML = JSON.stringify(classroom);
        classroomsDiv.appendChild(classroomDiv)
    });
}

main();
