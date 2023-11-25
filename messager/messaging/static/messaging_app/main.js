function sendMessage() {
    const message = document.getElementById('messageInput').value;
    const recipient = document.getElementById('recipientInput').value;

    const jsonData = {
        message: message,
        recipient: recipient
    };

    fetch('/send_message/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    })
        .then(handleResponse)
        .catch(handleError);
}
function handleKeyDown(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}
document.getElementById('messageInput').addEventListener('keydown', handleKeyDown);
document.getElementById('recipientInput').addEventListener('keydown', handleKeyDown);
function handleResponse(response) {
    if (response.ok) {
        console.log('Message received successfully');
        response.json().then(data => {
            console.log(data.recipient)
            // Update the text box with the received message
            if (data.recipient) {
                displayRecipientNotification(data.recipient);
            }
            else {
                const messageDiv = document.createElement('div');
                messageDiv.classList.add('message');
                messageDiv.textContent = data.message;

                // Append the message to the messageArea div
                const messageContainer = document.getElementById('messageArea');
                messageContainer.appendChild(messageDiv);
                messageContainer.scrollTop = messageContainer.scrollHeight;
                // Scroll to the bottom
                }
        });
    } else {
        console.error('Error sending message');
        // Logic for handling message sending error (if needed)
    }
}

function handleError(error) {
    console.error('Error:', error);
    // Logic for handling general errors (if needed)
}
function displayRecipientNotification(recipient) {
    const notification = document.getElementById('notification');
    notification.textContent = `Message will be sent only to recipient: ${recipient}`;
    notification.style.display = 'block';
    setTimeout(() => {
        notification.style.display = 'none';
    }, 5000); // 5000 milliseconds = 5 seconds
}