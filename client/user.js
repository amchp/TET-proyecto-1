let domain = "http://52.23.36.107"

function signup() {
    username = $("#signup-username").val()
    password = $("#signup-password").val()
    fetch(domain + "/User/new", {
        method: "POST",
        mode: "cors",
        redirect: "follow",
        body: JSON.stringify({"username": username, "password": password}),
        headers: {
            "Content-Type": "application/json"
        }
    }).then((res) => {
        res.json().then((data) => {
            console.log(data);
            $("#signup-text").text(JSON.stringify(data))
        });
    });
}

function listUsers() {
    username = $("#user-username").val()
    password = $("#user-password").val()
    fetch(domain + "/User/list?username=" + username + "&password=" + password, {
        method: "GET",
        mode: "cors",
        redirect: "follow"
    }).then((res) => {
        res.json().then((data) => {
            console.log(data);
            $("#user-text").text(JSON.stringify(data))
        });
    })
}

function deleteUser(){
    username = $("#signup-username").val()
    password = $("#signup-password").val()
    fetch(domain + "/User/delete", {
        method: "DELETE",
        mode: "cors",
        redirect: "follow",
        body: JSON.stringify({"username": username, "password": password}),
        headers: {
            "Content-Type": "application/json"
        }
    }).then((res) => {
        res.json().then((data) => {
            console.log(data);
            $("#user-text").text(JSON.stringify(data))
        });
    });
}

function usermethods() {
    choice = $("#user-route").val()
    if(choice == "list") listUsers();
    else if(choice == "delete") deleteUser();
    else $("#user-text").text("Please choose one method")
}
