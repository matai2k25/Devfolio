function toggleMenu() {
  document.getElementById("navMenu").classList.toggle("active");
}

document.addEventListener("DOMContentLoaded", () => {
  const scrollBox = document.querySelector(".scrollable-div");
  const input = document.querySelector(".chat-input");
  const sendBtn = document.querySelector(".send-btn");

  // Add a welcome message from the bot
  addBotMessage("Hi there! I'm MatAI 🤖. How can I help you today?");

  function reloadVideo() {
    const video = document.getElementById("myVideo");
    video.pause();          // Stop current playback
    video.currentTime = 0;  // Reset to start
    video.load();           // Reload the source
    video.play();           // Optional: auto-play again
  }

  sendBtn.addEventListener("click", () => {
    const userMsg = input.value.trim();
    if (userMsg === "") return;

    // Add user message
    addUserMessage(userMsg);
    

    // Show loading
    const loadingId = Date.now();
    addBotMessage(`<span id="loader-${loadingId}">MatAI is thinking<span class="dots-anim">...</span></span>`);

    const sourceElement = document.getElementById("videoSource");

    
    const currentSrc = sourceElement.getAttribute("src");

    fetch('/solution', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ name: userMsg })
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
    
      // Remove loading
      const loaderElem = document.getElementById(`loader-${loadingId}`);
      if (loaderElem) loaderElem.parentElement.parentElement.remove();
      reloadVideo();
    
      // Show real response from the backend
      addBotMessage(data.message);  // Here we use the message from the JSON response
      // ✅ These run AFTER the response is received
      sourceElement.setAttribute("src", `/static/renders/videos/generated_scene/480p15/MyScene.mp4?t=${Date.now()}`);
      const video = document.getElementById("myVideo");
      video.load();   // refreshes the video
      video.play(); 
      
    })
    .catch(error => {
      console.error('Error:', error);
    });

    input.value = "";
  });

  function addUserMessage(msg) {
    const userMsgHTML = `
      <div class="user-message">
        <div class="msg-box">
          <div class="right-name tab">
            <h1 class="title">User</h1>
          </div>
          <div class="tab left-tab">
            <div class="dots"><span></span><span></span><span></span></div>
          </div>
          <p>${msg}</p>
        </div>
      </div>
    `;
    scrollBox.insertAdjacentHTML("afterbegin", userMsgHTML);
    scrollToBottom();
  
  }
  
  function addBotMessage(msg) {
    const botMsgHTML = `
      <div class="bot-message">
        <div class="msg-box">
          <div class="bot-right-name tab">
            <h1 class="title">MatAI<span class="heart">♥</span></h1>
          </div>
          <div class="tab bot-left-tab">
            <div class="dots"><span></span><span></span><span></span></div>
          </div>
          ${msg}
        </div>
      </div>
    `;
    scrollBox.insertAdjacentHTML("afterbegin", botMsgHTML);
    scrollToBottom();
  }

  function scrollToBottom() {
    scrollBox.scrollTop = scrollBox.scrollHeight;
  }

  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      sendBtn.click();
    }
  });
  
});

