const apiURL = "http://127.0.0.1:8080";

const classroomDiv = document.getElementById("classroom");

async function getClasssroom(token, classroomID) {
    const response = await fetch(`${apiURL}/classroom/${classroomID}?token=${token}`);
    console.log("Get classroom endpoint responded with");
    console.log(response);
    const classroom = await response.json();
    console.log("Got the following classroom data");
    console.log(classroom)
    return classroom.classroom_data;
}

async function getUser(token, userID) {
    const response = await fetch(`${apiURL}/user/${userID}?token=${token}`);
    console.log("Get user endpoint responded with");
    console.log(response);
    const user = await response.json();
    console.log("Got the following user data");
    console.log(user);
    return user.user_data;
}

async function main() {
    const token = localStorage.getItem("token");
    const classroom = await getClasssroom(token, localStorage.getItem("currentClassroom"));
    console.log("Adding classroom: ");
    console.log(classroom);
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
    const owner = await getUser(token, classroom.owner_id);
    classroomOwnerSpan.innerHTML = "Owner: " + owner.name;
    classroomDiv.appendChild(classroomNameSpan);
    classroomDiv.appendChild(classroomSectionSpan);
    classroomDiv.appendChild(classroomOwnerSpan);
    if (classroom.code) {
        let classroomCodeSpan = document.createElement("span");
        classroomCodeSpan.className = "classroom-code-display";
        classroomCodeSpan.innerHTML = "Code: " + classroom.code;
        classroomDiv.appendChild(classroomCodeSpan);
    }
}

main();
