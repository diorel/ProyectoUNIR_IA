const sendButton = document.querySelector('#sendButton');
const inputElement = document.querySelector('#inputText');
const messagesContainer = document.querySelector('.chat__messages');
const userId = Date.now() + Math.random(777 + Math.random() * 7000);
const queryParams = window.location.search;
const urlParams = new URLSearchParams(queryParams);

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
    const inputText = inputElement.value.trim();
    let llmResponse = '';

    if (!inputText) return false;

    messagesContainer.innerHTML += `<div class="chat__message chat__message--user">Yo: ${inputText}</div>`;
    inputElement.value = '';
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    if (urlParams.get('llm') === 'llama') {
        llmResponse = await llamaApi(inputText);
    } else {
        llmResponse = await chatGPTApi(inputText);
    }

    if (llmResponse) {
        messagesContainer.innerHTML += `<div class="chat__message chat__message--bot">Carmen: ${llmResponse?.reply}</div>`;
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


