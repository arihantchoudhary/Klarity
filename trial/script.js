document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const userInput = document.getElementById('user-input');
    const sendButton = document.querySelector('.send-btn');
    const chatMessages = document.querySelector('.chat-messages');
    const sourceCheckboxes = document.querySelectorAll('.source-item input[type="checkbox"]');
    const allSourcesCheckbox = document.getElementById('all-sources');
    const suggestedQuestion = document.querySelector('.suggested-question p');
    const nextButton = document.querySelector('.next-btn');
    const loadButton = document.querySelector('.load-btn');
    const pfizerDirectorySelect = document.getElementById('pfizer-directory');
    const pfizerFilesContainer = document.getElementById('pfizer-files');
    const editorContent = document.querySelector('.editor-content');
    const toolbarButtons = document.querySelectorAll('.toolbar-btn');
    
    let currentEditingFile = null;
    let fileContents = new Map(); // Cache for file contents
    
    // Sample suggested questions
    const suggestedQuestions = [
        "How does dense vector indexing improve RAG performance?",
        "What techniques are used for efficient document retrieval?",
        "How does the system handle semantic search across 500+ documents?",
        "What are the advantages of vector-based document indexing?",
        "Can you explain the document processing pipeline?"
    ];
    let currentSuggestionIndex = 0;

    // Initial state
    allSourcesCheckbox.checked = true;
    sourceCheckboxes.forEach(checkbox => {
        checkbox.checked = true;
    });
    
    // Event Listeners
    
    // Handle toolbar button clicks
    toolbarButtons.forEach(button => {
        button.addEventListener('click', function() {
            const command = this.getAttribute('data-command');
            if (command) {
                document.execCommand(command, false, null);
            }
        });
    });
    
    // Handle file selection for editing
    function handleFileSelection(filePath) {
        if (currentEditingFile === filePath) return;
        
        currentEditingFile = filePath;
        
        // Show loading state
        editorContent.innerHTML = '<p>Loading document...</p>';
        
        // Fetch file contents
        fetch(`/api/file-contents?path=${encodeURIComponent(filePath)}`)
            .then(response => response.text())
            .then(content => {
                fileContents.set(filePath, content);
                editorContent.innerHTML = `<pre>${content}</pre>`;
            })
            .catch(error => {
                console.error('Error loading file:', error);
                editorContent.innerHTML = '<p>Error loading document. Please try again.</p>';
            });
    }
    
    // Auto-save edited content
    let saveTimeout;
    editorContent.addEventListener('input', function() {
        if (!currentEditingFile) return;
        
        clearTimeout(saveTimeout);
        saveTimeout = setTimeout(() => {
            const content = editorContent.innerText;
            
            fetch('/api/save-file', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    path: currentEditingFile,
                    content: content
                }),
            })
            .catch(error => {
                console.error('Error saving file:', error);
            });
        }, 1000);
    });
    
    // Send message when send button is clicked
    sendButton.addEventListener('click', sendMessage);
    
    // Send message when Enter key is pressed in input field
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Toggle all sources when "Select all sources" is clicked
    allSourcesCheckbox.addEventListener('change', function() {
        sourceCheckboxes.forEach(checkbox => {
            checkbox.checked = this.checked;
        });
    });
    
    // Update "Select all" checkbox state when individual checkboxes change
    sourceCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateSelectAllCheckbox);
    });
    
    // Show next suggested question when next button is clicked
    nextButton.addEventListener('click', showNextSuggestion);
    
    // Use suggested question when clicked
    suggestedQuestion.parentElement.addEventListener('click', useSuggestedQuestion);
    
    // Load conversation when load button is clicked
    loadButton.addEventListener('click', loadConversation);

    // Load Pfizer files when directory is selected
    pfizerDirectorySelect.addEventListener('change', function() {
        const selectedDir = this.value;
        if (!selectedDir) {
            pfizerFilesContainer.querySelector('.source-loading').textContent = 'Select a directory to load files...';
            return;
        }

        // Show loading state
        pfizerFilesContainer.querySelector('.source-loading').textContent = 'Loading files...';

        // Make API request to get files from the selected directory
        fetch(`/api/pfizer-files?directory=${selectedDir}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            // Clear existing files
            const existingFiles = pfizerFilesContainer.querySelectorAll('.source-item');
            existingFiles.forEach(file => file.remove());
            
            // Remove loading message
            const loadingMsg = pfizerFilesContainer.querySelector('.source-loading');
            if (loadingMsg) loadingMsg.remove();

            // Add new files
            data.files.forEach((file, index) => {
                const fileDiv = document.createElement('div');
                fileDiv.className = 'source-item';
                const filePath = `${selectedDir}/${file}`;
                fileDiv.innerHTML = `
                    <input type="checkbox" id="pfizer-${index}" value="${filePath}">
                    <label for="pfizer-${index}" class="file-label">
                        <i class="fas fa-file-pdf"></i> ${file}
                    </label>
                `;
                pfizerFilesContainer.appendChild(fileDiv);

                // Add click handler for editing
                const label = fileDiv.querySelector('.file-label');
                label.addEventListener('click', (e) => {
                    e.preventDefault();
                    handleFileSelection(filePath);
                });

                // Add the new checkbox to the sourceCheckboxes NodeList
                const checkbox = fileDiv.querySelector('input[type="checkbox"]');
                checkbox.addEventListener('change', updateSelectAllCheckbox);
            });

            // Update the select all checkbox state
            updateSelectAllCheckbox();
        })
        .catch(error => {
            console.error('Error loading Pfizer files:', error);
            pfizerFilesContainer.querySelector('.source-loading').textContent = 'Error loading files. Please try again.';
        });
    });

    // Functions
    
    function sendMessage() {
        const message = userInput.value.trim();
        if (message) {
            // Add user message to chat
            addMessageToChat('user', message);
            
            // Clear input field
            userInput.value = '';
            
            // Send message to server and get response
            fetchBotResponse(message);
        }
    }
    
    function addMessageToChat(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        if (sender === 'user') {
            // User message
            messageDiv.innerHTML = `
                <div class="message-icon">
                    <i class="fas fa-user user-icon"></i>
                </div>
                <div class="message-content">
                    <div class="message-text">
                        <p>${text}</p>
                    </div>
                </div>
            `;
        } else {
            // Bot message
            messageDiv.innerHTML = `
                <div class="message-icon">
                    <i class="fas fa-brain brain-icon"></i>
                </div>
                <div class="message-content">
                    <div class="message-text">
                        <p>${text}</p>
                    </div>
                </div>
            `;
        }
        
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom of chat
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function fetchBotResponse(message) {
        // Get selected sources including Pfizer files
        const selectedSources = Array.from(document.querySelectorAll('.source-item input[type="checkbox"]:checked'))
            .map(checkbox => {
                if (checkbox.id.startsWith('pfizer-')) {
                    return checkbox.value; // This will be the full path: directory/filename
                }
                return checkbox.id;
            });
        
        // Show loading indicator
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message system-message loading';
        loadingDiv.innerHTML = `
            <div class="message-icon">
                <i class="fas fa-brain brain-icon"></i>
            </div>
            <div class="message-content">
                <div class="message-text">
                    <p>Searching across documents...</p>
                </div>
            </div>
        `;
        chatMessages.appendChild(loadingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Make API request to the backend
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                sources: selectedSources
            }),
        })
        .then(response => response.json())
        .then(data => {
            // Remove loading indicator
            chatMessages.removeChild(loadingDiv);
            
            // Add bot response to chat
            addMessageToChat('system', data.response);
        })
        .catch(error => {
            console.error('Error:', error);
            
            // Remove loading indicator
            chatMessages.removeChild(loadingDiv);
            
            // Add error message to chat
            addMessageToChat('system', 'Sorry, there was an error processing your request. Please try again.');
        });
    }
    
    function updateSelectAllCheckbox() {
        const allChecked = Array.from(sourceCheckboxes).every(checkbox => checkbox.checked);
        const someChecked = Array.from(sourceCheckboxes).some(checkbox => checkbox.checked);
        
        allSourcesCheckbox.checked = allChecked;
        allSourcesCheckbox.indeterminate = someChecked && !allChecked;
    }
    
    function showNextSuggestion() {
        currentSuggestionIndex = (currentSuggestionIndex + 1) % suggestedQuestions.length;
        suggestedQuestion.textContent = suggestedQuestions[currentSuggestionIndex];
    }
    
    function useSuggestedQuestion() {
        userInput.value = suggestedQuestions[currentSuggestionIndex];
        userInput.focus();
    }
    
    function loadConversation() {
        const loadBtn = document.querySelector('.load-btn');
        loadBtn.textContent = 'Loading...';
        
        // Simulate loading delay
        setTimeout(() => {
            loadBtn.textContent = 'Loaded';
            
            // Add system message after loading
            const systemMessage = 'Document index loaded successfully. You can now query across all documents.';
            addMessageToChat('system', systemMessage);
            
            // Reset button after a delay
            setTimeout(() => {
                loadBtn.textContent = 'Load';
            }, 2000);
        }, 1500);
    }

    // Initial suggested question
    suggestedQuestion.textContent = suggestedQuestions[0];
});
