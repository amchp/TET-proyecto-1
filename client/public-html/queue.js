function sendMessage() {
    username = $("#queue-username").val()
    password = $("#queue-password").val()
    queue = $("#queue-queue").val()
    message = $("#queue-message").val()
    fetch(domain + "/Queue/send", {
        method: "POST",
        mode: "cors",
        redirect: "follow",
        body: JSON.stringify({"username": username, "password": password, "queue": queue, "message": message}),
        headers: {
            "Content-Type": "application/json"
        }
    }).then((res) => {
        res.json().then((data) => {
            console.log(data);
            $("#queue-text").text(JSON.stringify(data))
        });
    });
}

function retrieveMessages(){
    username = $("#queue-username").val()
    password = $("#queue-password").val()
    fetch(domain + "/Queue/retrieve", {
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
            $("#queue-text").text(JSON.stringify(data))
        });
    });
}

function createQueue(){
    username = $("#queue-username").val()
    password = $("#queue-password").val()
    receiver = $("#queue-receiver").val()
    fetch(domain + "/Queue/new", {
        method: "POST",
        mode: "cors",
        redirect: "follow",
        body: JSON.stringify({"username": username, "password": password, "receiver": receiver}),
        headers: {
            "Content-Type": "application/json"
        }
    }).then((res) => {
        res.json().then((data) => {
            console.log(data);
            $("#queue-text").text(JSON.stringify(data))
        });
    });
}

function deleteQueue(){
    username = $("#queue-username").val()
    password = $("#queue-password").val()
    queue = $("#queue-queue").val()
    fetch(domain + "/Queue/delete", {
        method: "DELETE",
        mode: "cors",
        redirect: "follow",
        body: JSON.stringify({"username": username, "password": password, "queue": queue}),
        headers: {
            "Content-Type": "application/json"
        }
    }).then((res) => {
        res.json().then((data) => {
            console.log(data);
            $("#queue-text").text(JSON.stringify(data))
        });
    });
}

function listQueues(){
    username = $("#queue-username").val()
    password = $("#queue-password").val()
    fetch(domain + "/Queue/list?username=" + username + "&password=" + password, {
        method: "GET",
        mode: "cors",
        redirect: "follow",
    }).then((res) => {
        res.json().then((data) => {
            console.log(data);
            $("#queue-text").text(JSON.stringify(data))
        });
    });
}

function queuemethods(){
    choice = $("#queue-route").val()
    if(choice == "send") sendMessage();
    else if(choice == "retrieve") retrieveMessages();
    else if(choice == "new") createQueue();
    else if(choice == "list") listQueues();
    else if(choice == "delete") deleteQueue();
    else $("#queue-text").text("Please choose one method");
}

function hideQueue() {
    $("#queue-u").hide()
    $("#queue-p").hide()
    $("#queue-q").hide()
    $("#queue-m").hide()
    $("#queue-r").hide()
}

function queueChange() {
    choice = $("#queue-route").val()
    hideQueue()
    if(choice == "send"){
        $("#queue-u").show()
        $("#queue-p").show()
        $("#queue-q").show()
        $("#queue-m").show()
    }
    else if(choice == "retrieve"){
        $("#queue-u").show()
        $("#queue-p").show()
    }
    else if(choice == "new"){
        $("#queue-u").show()
        $("#queue-p").show()
        $("#queue-r").show()
    }
    else if(choice == "list"){
        $("#queue-u").show()
        $("#queue-p").show()
    }
    else if(choice == "delete"){
        $("#queue-u").show()
        $("#queue-p").show()
        $("#queue-q").show()
    }
}