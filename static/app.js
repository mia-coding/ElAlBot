const chat = document.getElementById('chat');
const input = document.getElementById('userInput');

function appendMessage(text, sender) {
  const msg = document.createElement('div');
  msg.className = `message ${sender}`;
  msg.textContent = text;
  chat.appendChild(msg);
  chat.scrollTop = chat.scrollHeight;
}

async function sendMessage() {
  const userText = input.value.trim();
  if (!userText) return;

  appendMessage(userText, 'user');
  input.value = '';

  try {
    const response = await fetch('/send_message', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userText })
    });
    const data = await response.json();
    appendMessage(data.response, 'bot');
  } catch (err) {
    appendMessage('Oops! Something went wrong.', 'bot');
  }
}

input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') sendMessage();
});