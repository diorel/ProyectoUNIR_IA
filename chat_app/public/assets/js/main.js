const sendButton = document.querySelector('#sendButton');
const inputElement = document.querySelector('#inputText');
const messagesContainer = document.querySelector('.chat__messages');
const userId = Date.now() + Math.random(777 + Math.random() * 7000);


const sendMessage = async () => {
    // Sacar el valor del input (pregunta)

    const inputText = inputElement.value.trim();

    if (!inputText) return false;

    // Meter mensaje del usuario en la caja de mensajes

    messagesContainer.innerHTML += `<div class="chat__message chat__message--user">Yo: ${inputText}</div>`;

    // Vaciar el input del usuario
    inputElement.value = '';

    // Petición al backend para que me responda la IA
    try {
        const response = await fetch('/api/chatbot', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                userId,
                message: inputText }),
        });

        // Incrustar mensaje del bot en el chat
        const data = await response.json();
        messagesContainer.innerHTML += `<div class="chat__message chat__message--bot">Carmen: ${data.reply}</div>`;
    } catch (error) {
        console.log(error);
    }

    // Mover el scroll hacia abajo
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

sendButton.addEventListener('click', sendMessage);
inputElement.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        sendMessage();
    }
});


