function sendMessage() {
    const message = document.getElementById('messageInput').value;
    const recipient = document.getElementById('recipientInput').value;
    if (!message) {
        displayEmptyMessageNotification();
        return; // Prevent sending if the message is empty
    }
    const jsonData = {
        message: message,
        recipient: recipient
    };

    fetch('send_message/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    })
        .then(handleMessageResponse)
        .catch(handleError);
}
function handleKeyDown(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}
document.getElementById('messageInput').addEventListener('keydown', handleKeyDown);
document.getElementById('recipientInput').addEventListener('keydown', handleKeyDown);
function handleMessageResponse(response) {
    if (response.ok) {
        console.log('Message received successfully');
        response.json().then(data => {
            console.log(data.recipient)
            // Update the text box with the received message
            if (data.recipient) {
                displayRecipientNotification(data.recipient);
            }
            else {
                if(!data.message || !data.sender_name || !data.sender_code)
                    return
                const messageDiv = document.createElement('div');
                messageDiv.classList.add('message');
                messageDiv.textContent =`[${data.sender_code}] ${data.sender_name}: ${data.message}`
                // Append the message to the messageArea div
                const messageContainer = document.getElementById('messageArea');
                messageContainer.appendChild(messageDiv);
                messageContainer.scrollTop = messageContainer.scrollHeight;
                // Scroll to the bottom
                }
        });
    } else {
        displayErrorNotification(response)
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

function displayEmptyMessageNotification() {
    const notification = document.getElementById('notification');
    notification.textContent = 'Message cannot be empty!';
    notification.style.display = 'block';
    setTimeout(() => {
        notification.style.display = 'none';
    }, 5000); // 5000 milliseconds = 5 seconds
}
function displayErrorNotification(response) {
    response.json().then(message_data => {
        const notification = document.getElementById('notification');
        notification.textContent = message_data.error_message;
        notification.style.display = 'block';
        setTimeout(() => {
            notification.style.display = 'none';
        }, 5000); // 5000 milliseconds = 5 seconds
    })
}



//SIDE COLUMN JS
// Function to fetch online users
function fetchOnlineUsers() {
    // Make an API call to your backend to fetch online users
    // Replace this with your actual endpoint for fetching online users
    fetch('get_online_users/')
        .then(response => response.json())
        .then(data => {
            console.log(data)
            // Call a function to display the online users
            displayOnlineUsers(data.online_users);
        })
        .catch(error => {
            console.error('Error fetching online users:', error);
        });
}
// Function to display online users
function displayOnlineUsers(onlineUsers) {
    const onlineUsersList = document.getElementById('onlineUsersList');
    onlineUsersList.innerHTML = '';
    console.log(typeof onlineUsers)
    onlineUsers.forEach(user => {
        const li = document.createElement('li');
        li.textContent = `#${user.usercode}: ${user.username}`;
        li.classList.add('online-user');

        // Add a click event listener to each list item
        li.addEventListener('click', () => {
            // Handle clicking on a user (e.g., send a message, etc.)
            // You can add your logic here
            console.log(`Clicked on ${user.username}`);
        });

        onlineUsersList.appendChild(li);
    });
}

// Function to refresh online users every 30 seconds
function refreshOnlineUsers() {
    fetchOnlineUsers(); // Initial fetch
    setInterval(fetchOnlineUsers, 30000); // Fetch every 30 seconds
}

// Call the function to refresh online users
refreshOnlineUsers();

// Refresh from Icon
document.getElementById('refreshIcon').addEventListener('click', function() {
    // Call your refresh function here or perform the necessary actions
    refreshOnlineUsers(); // Replace 'refreshUserList' with your actual refresh function
});


// Historical Requests:
function fetchHistoricalMessages() {
    fetch('fetch_historical_messages/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Handle the received historical messages
        displayHistoricalMessages(data.last_messages);
    })
    .catch(error => {
        console.error('Error fetching historical messages:', error);
    });
}

// Call fetchHistoricalMessages when the page loads or when needed
// For example, on initial page load:
window.onload = function() {
    fetchHistoricalMessages();
    // Other initialization logic
}

function displayHistoricalMessages(historicalMessages) {
    historicalMessages.forEach(message => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.textContent = `[${message.sender_code}] ${message.sender_name}: ${message.message}`;

        const messageContainer = document.getElementById('messageArea');
        messageContainer.appendChild(messageDiv);
        messageContainer.scrollTop = messageContainer.scrollHeight;
    });
}