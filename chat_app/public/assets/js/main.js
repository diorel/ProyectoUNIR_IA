const sendButton = document.querySelector('#sendButton');
const inputElement = document.querySelector('#inputText');
const quickQuestionList = document.getElementById('quick_questions_list');
const messagesContainer = document.querySelector('.chat__messages');
const userId = Date.now() + Math.random(777 + Math.random() * 7000);
const urlParams = new URLSearchParams(window?.location?.search);

const llamaApi = async (message) => {
    try {
        const response = await fetch('/api/llama', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                userId,
                message 
            })
        });
        const data = await response.json();
        return data;
    } catch (error) {
        throw new Error(`There has been an error with the api: ${error}`);
    }
}

const chatGPTApi = async (message) => {
    try {
        const response = await fetch('/api/chatbot', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                userId,
                message 
            })
        });

        return await response.json();
    } catch (error) {
        throw new Error(`There has been an error with the api: ${error}`);
    }
}

const sendMessage = async () => {
    let llmResponse = '';
    const inputText = inputElement.value.trim();

    if (!inputText) return false;

    // Agregar mensaje del usuario al chat
    messagesContainer.innerHTML += `<div class="chat__message chat__message--user">Yo: ${inputText}</div>`;

    // Vaciar el input del usuario
    inputElement.value = '';

    // Mostrar animación de carga
    const loadingMessage = document.createElement('div');
    loadingMessage.classList.add('chat__message', 'chat__message--loading');
    loadingMessage.innerHTML = 'Carmen está escribiendo...';
    messagesContainer.appendChild(loadingMessage);

    // Mover el scroll hacia abajo
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    try {
        // Petición al backend para obtener la respuesta
        if (urlParams.get('llm') === 'llama') {
            llmResponse = await llamaApi(inputText);
        } else {
            llmResponse = await chatGPTApi(inputText);
        }

        // Eliminar animación de carga
        loadingMessage.remove();

        // Mostrar respuesta del bot
        messagesContainer.innerHTML += `<div class="chat__message chat__message--bot">Carmen: ${llmResponse?.reply}</div>`;
    } catch (error) {
        console.error(error);

        // Eliminar animación de carga
        loadingMessage.remove();

        // Mostrar mensaje de error
        messagesContainer.innerHTML += `<div class="chat__message chat__message--bot">Carmen: Hubo un error al procesar tu solicitud.</div>`;
    }

    // Mover el scroll hacia abajo
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
};

sendButton.addEventListener('click', sendMessage);
inputElement.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

quickQuestionList.addEventListener('click', function(evt){
    if(evt?.target?.tagName === 'LI') {
        inputElement.value = evt?.target?.textContent;
        sendMessage();
    }
});

