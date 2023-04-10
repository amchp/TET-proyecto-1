function sendMessage() {
    username = $("#topic-username").val()
    password = $("#topic-password").val()
    topic = $("#topic-topic").val()
    message = $("#topic-message").val()
    fetch(domain + "/Topic/send", {
        method: "POST",
        mode: "cors",
        redirect: "follow",
        body: JSON.stringify({"username": username, "password": password, "topic": topic, "message": message}),
        headers: {
            "Content-Type": "application/json"
        }
    }).then((res) => {
        res.json().then((data) => {
            console.log(data);
            $("#topic-text").text(JSON.stringify(data))
        });
    });
}

function subscribeToTopic() {
    username = $("#topic-username").val()
    password = $("#topic-password").val()
    topic = $("#topic-topic").val()
    fetch(domain + "/Topic/subscribe", {
        method: "POST",
        mode: "cors",
        redirect: "follow",
        body: JSON.stringify({"username": username, "password": password, "topic": topic}),
        headers: {
            "Content-Type": "application/json"
        }
    }).then((res) => {
        res.json().then((data) => {
            console.log(data);
            $("#topic-text").text(JSON.stringify(data))
        });
    });
}

function unsubscribeFromTopic() {
    username = $("#topic-username").val()
    password = $("#topic-password").val()
    topic = $("#topic-topic").val()
    fetch(domain + "/Topic/unsubscribe", {
        method: "POST",
        mode: "cors",
        redirect: "follow",
        body: JSON.stringify({"username": username, "password": password, "topic": topic}),
        headers: {
            "Content-Type": "application/json"
        }
    }).then((res) => {
        res.json().then((data) => {
            console.log(data);
            $("#topic-text").text(JSON.stringify(data))
        });
    });
}

function listTopics() {
    fetch(domain + "/Topic/list", {
        method: "GET",
        mode: "cors",
        redirect: "follow"
    }).then((res) => {
        res.json().then((data) => {
            console.log(data);
            $("#topic-text").text(JSON.stringify(data))
        });
    });
}

function topicmethods() {
    choice = $("#topic-route").val()
    if(choice == "send") sendMessage();
    else if(choice == "subscribe") subscribeToTopic();
    else if(choice == "unsubscribe") unsubscribeFromTopic();
    else if(choice == "list") listTopics();
    else $("#topic-text").text("Please choose one method")
}

function hideTopic() {
    $("#topic-u").hide()
    $("#topic-p").hide()
    $("#topic-t").hide()
    $("#topic-m").hide()
}

function topicChange() {
    choice = $("#topic-route").val()
    hideTopic()
    if(choice == "send"){
        $("#topic-u").show()
        $("#topic-p").show()
        $("#topic-t").show()
        $("#topic-m").show()
    }
    else if(choice == "subscribe"){
        $("#topic-u").show()
        $("#topic-p").show()
        $("#topic-t").show()
    }
    else if(choice == "unsubscribe"){
        $("#topic-u").show()
        $("#topic-p").show()
        $("#topic-t").show()
    }
}