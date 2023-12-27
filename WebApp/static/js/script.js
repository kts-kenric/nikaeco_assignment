const submitButton = document.getElementById("submit-button");
const userInput = document.getElementById('user_input');

document.addEventListener("DOMContentLoaded", function () {

    document.getElementById("uploadForm").addEventListener("submit", function(event) {
        event.preventDefault();
    
        const files = document.getElementById('fileInput').files;
        const formData = new FormData();
    
        for (let i = 0; i < files.length; i++) {
            formData.append('file', files[i]);
        }
    
        fetch('http://127.0.0.1:4000/upload', {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Upload failed');
            }
        })
        .then(data => {
            console.log('Files uploaded successfully:', data);
            setTimeout(function() {
                // Perform actions after successful file upload (here, just showing the "File uploaded successfully!" label)
                fileUploadedLabel.style.display = 'block'; // Display the label
                fileInput.value = ''; // Clear the file input (optional)
            }, 2000); 
            // Perform further actions if needed with the response data
        })
        .catch(error => {
            console.error('Error:', error);
            // Handle errors or display an error message
        });
    });


    userInput.addEventListener('keyup', function(event) {
        // Check if the 'Enter' key is pressed (key value 'Enter')
        if (event.key === 'Enter') {
            // Prevent the default form submission behavior
            event.preventDefault();

            // Trigger a click on the submit button
            submitButton.click();
        }
    });

    submitButton.addEventListener("click", function () {
        submitButton.disabled = true;
        var userInput = document.querySelector('input[id="user_input"]');

        if (!userInput || userInput.value == ''){
            console.log('Input element with name "user_input" not found.');
            submitButton.disabled = false;
        }
        else{
            // Check if the element was found
                // Accessing the input value
            appendUserChatMessage(userInput.value)
            //userinputVal = userInput.value
            console.log(userInput.value); // Retrieves the current value

            // Modifying the input value
             // Sets a new value
            var formdata = new FormData();
            formdata.append("user_input", userInput.value);
            userInput.value ='';
            // Adding an event listener (e.g., keyup event)
            // userInput.addEventListener('keyup', function(event) {
            //     console.log('Key pressed:', event.key);
            //     // Other actions based on key events can be performed here
            // });
            fetch("http://127.0.0.1:4000/input", {
                method: 'POST',
                body: formdata,
            }).then(function(response) {
                if (response.ok) {
                    return response.text(); // Extract text content from the response
                } else {
                    console.log('Server returned an error: ' + response.status);
                    throw new Error('Server returned an error');
                    submitButton.disabled = false;

                }
            }).then(function(textData) {
                // Handle the text data received from the server
                console.log('Received text from the server:', textData);

                appendBotChatMessage(textData)

                submitButton.disabled = false;

                // Perform actions based on the text data here
            }).catch(function(error) {
                console.error('Fetch error:', error);
                submitButton.disabled = false;

            });

            submitButton.disabled = false;
        }
    });
});


function appendUserChatMessage(userMessage) {
    var chatContainer = document.getElementById('chat-container');

    var userMessageDiv = document.createElement('div');
    userMessageDiv.classList.add('message', 'user-message');

    var userParagraphHeader = document.createElement('p');
    userParagraphHeader.textContent = 'User:';
    userMessageDiv.appendChild(userParagraphHeader);

    var userParagraph = document.createElement('p');
    userParagraph.textContent = userMessage;
    userMessageDiv.appendChild(userParagraph);

    chatContainer.appendChild(userMessageDiv);

}


function appendBotChatMessage(botMessage) {
    var botMessageDiv = document.createElement('div');
    botMessageDiv.classList.add('message', 'bot-message');

    var botParagraphHeader = document.createElement('p');
    botParagraphHeader.textContent = 'Bot:';
    botMessageDiv.appendChild(botParagraphHeader);

    var lines = botMessage.split('\n');
    lines.forEach(function(line) {
        var paragraph = document.createElement('p');
        paragraph.textContent = line;
        botMessageDiv.appendChild(paragraph);
    });

    chatContainer.appendChild(botMessageDiv);
}

// function appendChatMessage(userMessage, botMessage) {
//     var chatContainer = document.getElementById('chat-container');

//     var userMessageDiv = document.createElement('div');
//     userMessageDiv.classList.add('message', 'user-message');

//     var userParagraphHeader = document.createElement('p');
//     userParagraphHeader.textContent = 'User:';
//     userMessageDiv.appendChild(userParagraphHeader);

//     var userParagraph = document.createElement('p');
//     userParagraph.textContent = userMessage;
//     userMessageDiv.appendChild(userParagraph);

//     chatContainer.appendChild(userMessageDiv);

//     var botMessageDiv = document.createElement('div');
//     botMessageDiv.classList.add('message', 'bot-message');

//     var botParagraphHeader = document.createElement('p');
//     botParagraphHeader.textContent = 'Bot:';
//     botMessageDiv.appendChild(botParagraphHeader);

//     var lines = botMessage.split('\n');
//     lines.forEach(function(line) {
//         var paragraph = document.createElement('p');
//         paragraph.textContent = line;
//         botMessageDiv.appendChild(paragraph);
//     });

//     chatContainer.appendChild(botMessageDiv);
// }
