const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const messages = document.getElementById("messages");
const typing = document.getElementById("typing");

let typingInterval = null;
let dots = 0;

/* =========================
   EVENT LISTENERS
========================= */

sendBtn.addEventListener("click", sendMessage);

input.addEventListener("keypress", function(e){
    if(e.key === "Enter"){
        sendMessage();
    }
});


/* =========================
   ADD MESSAGE
========================= */

function addMessage(text, type){

    const msg = document.createElement("div");

    msg.classList.add("message", type);

    msg.textContent = text;

    msg.style.opacity = "0";
    msg.style.transform = "translateY(10px)";

    messages.appendChild(msg);

    setTimeout(()=>{
        msg.style.transition = "all 0.25s ease";
        msg.style.opacity = "1";
        msg.style.transform = "translateY(0)";
    },10);

    scrollBottom();
}


/* =========================
   SCROLL
========================= */

function scrollBottom(){
    messages.scrollTop = messages.scrollHeight;
}


/* =========================
   TYPING ANIMATION
========================= */

function startTyping(){

    typing.classList.remove("hidden");

    dots = 0;

    typingInterval = setInterval(()=>{

        dots = (dots + 1) % 4;

        typing.textContent = "Assistant is typing" + ".".repeat(dots);

    },400);
}


function stopTyping(){

    clearInterval(typingInterval);

    typingInterval = null;

    typing.classList.add("hidden");

    typing.textContent = "Assistant is typing";
}


/* =========================
   SEND MESSAGE
========================= */

async function sendMessage(){

    const text = input.value.trim();

    if(text === "") return;

    addMessage(text,"user");

    input.value = "";
    input.focus();

    startTyping();

    sendBtn.disabled = true;
    sendBtn.innerText = "Sending...";

    try{

        const response = await fetch("/api/chat",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({message:text})
        });

        const data = await response.json();

        stopTyping();

        const reply =
            data.reply ||
            data.error ||
            "Something went wrong.";

        addMessage(reply,"bot");

    }
    catch(error){

        stopTyping();

        addMessage("⚠️ Server error. Try again.","bot");

    }
    finally{

        sendBtn.disabled = false;
        sendBtn.innerText = "Send";

    }

}