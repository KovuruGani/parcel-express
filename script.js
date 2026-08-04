let registerForm = document.getElementById("registerForm");

if (registerForm) {

    registerForm.addEventListener("submit", async function(e) {

        e.preventDefault();

        let name = document.getElementById("name").value;
        let email = document.getElementById("email").value;
        let phone = document.getElementById("phone").value;
        let password = document.getElementById("password").value;
        let confirmPassword = document.getElementById("confirmPassword").value;

        if (password !== confirmPassword) {
            document.getElementById("message").innerHTML =
            "❌ Passwords do not match";
            return;
        }

        let response = await fetch("https://parcel-express-4.onrender.com/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: name,
                email: email,
                password: password
            })
        });

        let result = await response.json();

        document.getElementById("message").innerHTML = result.message;

    });

}
let loginForm = document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", async function(e) {

        e.preventDefault();

        let email = document.getElementById("loginEmail").value;
        let password = document.getElementById("loginPassword").value;

        let response = await fetch("https://parcel-express-4.onrender.com/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        let result = await response.json();

        document.getElementById("loginMessage").innerHTML = result.message;

        if (result.message === "Login Successful") {
            setTimeout(() => {
                window.location.href = "dashboard.html";
            }, 1000);
        }

    });

}
let bookForm = document.getElementById("bookForm");

if(bookForm){

bookForm.addEventListener("submit",async function(e){

e.preventDefault();
let sender = document.getElementById("sender").value;
let receiver = document.getElementById("receiver").value;
let pickup = document.getElementById("pickup").value;
let delivery = document.getElementById("delivery").value;
let weight = document.getElementById("weight").value;

if(sender=="" || receiver=="" || pickup=="" || delivery=="" || weight==""){
    alert("please fill all fields.");
    return;
}
if(isNaN(weight) || weight<=0){
    alert("Enter a valid weight.");
    return;
}

let response = await fetch("https://parcel-express-4.onrender.com/book", {

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

sender:sender,
receiver:receiver,
pickup:pickup,
delivery:delivery,
weight:weight

})

});

let result=await response.json();

document.getElementById("bookMessage").innerHTML=result.message;

});
}
function trackParcel() {

    let id = document.getElementById("parcelId").value;
    if(id==""){
        alert("please enter parcel ID");
        return;
    }

    fetch("https://parcel-express-4.onrender.com/track/" + id)
    .then(response => response.json())
    .then(data => {

        if(data.status){

            document.getElementById("result").innerHTML =
            "Status : " + data.status;

        }else{

            document.getElementById("result").innerHTML =
            "Parcel Not Found";

        }

    });

}

