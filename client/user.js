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
        return res;
    }).then((data) => {
        $("#signup-text").html(data)
    });
}
function hello(){
    console.log("A")
    fetch(domain + "/Topic/unsubscribe", {
        method: "POST",
        mode: "cors",
        redirect: "follow",
        body: JSON.stringify({"username": "jdbuenol", "password": "123", "topic": "Beach"}),
        headers: {
            "Content-Type": "application/json"
        }
    }).then((res) => {
        res.json().then((data) => {
            console.log(data);
        });
    });
}

function hello2(){
    console.log("B")

    fetch(domain + "/Topic/list", {
        method: "GET",
        mode: "cors",
        redirect: "follow"
    }).then((res) => {
        res.json().then((data) => {
            console.log(data);
        });
    });
}

function hello3(){
    console.log("C")
    $.ajax({
        url: domain + "/Queue/list",
        method: "Get",
        data: {"username": "jdbuenol", "password": "123"}
    }).done(function( data ) {
        console.log(data);
    });
}