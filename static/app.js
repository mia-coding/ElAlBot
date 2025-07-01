const chat = document.getElementById('chat');
const input = document.getElementById('userInput');
const sidebar = document.getElementById('sidebar');
const toggleBtn = document.getElementById('toggleSidebar');

function first_message(time = null) {
  message = "Hi, welcome! What question do you have?"
  const msg = document.createElement('div');
  msg.className = `message bot`;
  msg.innerHTML = `
    <span>${text}</span>
    <div style="font-size: 0.75rem; color: #ffffff}; margin-top: 4px; text-align: right;">
      ${time || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
    </div>
  `;
}

function appendMessage(text, sender, time = null) {
  const msg = document.createElement('div');
  msg.className = `message ${sender}`;
  time_color = "000000";
  if (sender === 'bot') {
    msg.classList.add('animated');
    time_color = "ffffff";
  }

  msg.innerHTML = `
    <span>${text}</span>
    <div style="font-size: 0.75rem; color: ${time_color}; margin-top: 4px; text-align: right;">
      ${time || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
    </div>
  `;

  chat.appendChild(msg);
  chat.scrollTop = chat.scrollHeight;
}

  let sidebarVisible = true;

async function sendMessage() {
  const userText = input.value.trim();
  if (!userText) return;
  const userList = userText.split("\\s+");
  let userResponse = "";
  for (let i = 0; i < userList.length ; i++)
  {
    userResponse = userResponse+userList[i] + " ";
    if (((userResponse.length % 8) === 0) && userResponse.length > 8) {
      userResponse = userResponse + "/n";
    }
  }
  appendMessage(userResponse, 'user');
  input.value = '';

  try {
    fetch('https://miacoding.pythonanywhere.com', { // <-- IMPORTANT: Update this URL!
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
    })
    .then(response => response.json())
    .then(data => {
        // Handle bot response
    })
    .catch(error => {
        console.error('Error:', error);
    });
    const response = await fetch('/get_response', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userResponse })
    });
    const data = await response.json();

    // Convert plain URLs into clickable links
    const withLinks = data.response.replace(
      /(https?:\/\/[^\s]+)/g,
      '<a href="$1" target="_blank" style="color: #fff; text-decoration: underline;">$1</a>'
    );

    appendMessage(withLinks, 'bot');
  } catch (err) {
    appendMessage('Oops, sorry... An error occurred.', 'bot');
  }
}

input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') sendMessage();
});