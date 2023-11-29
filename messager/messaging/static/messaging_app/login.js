// Login
document.getElementById('loginForm').addEventListener('submit', async function (event) {
    event.preventDefault(); // Prevent the default form submission behavior
    const form = event.target;
    const formData = new FormData(form);

    // Convert form data to JSON object
    const jsonData = {
        username: formData.get('username'),
        password: formData.get('password')
    };
    console.log(jsonData);
    try {
        const response = await fetch('login_user/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(jsonData),
        })
        if (response.redirected)
             window.location.replace('/messager/');
        else {
            displayNotification(response)
        }

    } catch (error) {
        console.error('Error:', error.message);
    }
});

//  register
document.getElementById('registerForm').addEventListener(
    'submit', async function (event) {
        event.preventDefault(); // Prevent the default form submission

        const form = event.target;
        const formData = new FormData(form);

        const jsonData = {
            username: formData.get('username'),
            password: formData.get('password'),
            email: formData.get('email')
        };
        console.log(jsonData)
        cookie = getCookie('csrftoken')
        console.log(cookie)

        try {
            const response = await fetch('register_user/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': cookie
                },
                body: JSON.stringify(jsonData)
            });
            const responseMessage = document.getElementById('registerResponseMessage');
            console.log(response)
            if (response.ok) {
                responseMessage.textContent = 'Registration successful!';
            } else {
                responseMessage.textContent = 'Registration failed. Please try again.';
            }
        } catch (error) {
            console.error('Error:', error.message);
        }
    });

// Function to retrieve the CSRF token from cookies
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
}

function displayNotification(response) {
    response.json().then(message_data => {
        const notification = document.getElementById('notification');
        notification.textContent = message_data.error_message;
        notification.style.display = 'block';
        setTimeout(() => {
            notification.style.display = 'none';
        }, 5000); // 5000 milliseconds = 5 seconds
    })
}
