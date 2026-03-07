const input = document.getElementById("user-input")
const sendBtn = document.getElementById("send-btn")
const messages = document.getElementById("messages")
const typing = document.getElementById("typing")

sendBtn.onclick = sendMessage

input.addEventListener("keypress", function(e){
if(e.key === "Enter"){
sendMessage()
}
})

function addMessage(text, type){

let div = document.createElement("div")

div.classList.add("message")
div.classList.add(type)

div.innerText = text

messages.appendChild(div)

messages.scrollTop = messages.scrollHeight

}

async function sendMessage(){

let message = input.value.trim()

if(message === "") return

addMessage(message,"user")

input.value=""

typing.classList.remove("hidden")

try{

const response = await fetch("/api/chat",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
message:message
})

})

const data = await response.json()

typing.classList.add("hidden")

let reply = data.reply || data.error || "Something went wrong"

addMessage(reply,"bot")

}catch(err){

typing.classList.add("hidden")

addMessage("Server error. Please try again.","bot")

}

}