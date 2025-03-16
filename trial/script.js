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
    const fileUpload = document.getElementById('file-upload');
    const folderUpload = document.getElementById('folder-upload');
    const uploadProgress = document.getElementById('upload-progress');
    const progressBar = document.querySelector('.progress-fill');
    const progressText = document.querySelector('.progress-text');
    const documentsContainer = document.getElementById('documents-container');
    const documentSearch = document.getElementById('document-search');
    const fileTypeFilter = document.getElementById('file-type-filter');
    const viewerContent = document.getElementById('viewer-content');
    const currentDocument = document.getElementById('current-document');
    const prevPageBtn = document.getElementById('prev-page');
    const nextPageBtn = document.getElementById('next-page');
    const pageInfo = document.getElementById('page-info');
    const zoomInBtn = document.getElementById('zoom-in');
    const zoomOutBtn = document.getElementById('zoom-out');
    const saveDocument = document.getElementById('save-document');
    const chatInput = document.getElementById('chat-input');
    const sendMessage = document.getElementById('send-message');
    
    let currentEditingFile = null;
    let fileContents = new Map(); // Cache for file contents
    let currentDocumentIndex = -1;
    let currentPage = 1;
    let totalPages = 1;
    let zoomLevel = 1;
    let processingFiles = false;
    let documents = [];
    let hasDocuments = false;
    
    // Sample suggested questions
    const suggestedQuestions = [
        "How does dense vector indexing improve RAG performance?",
        "What techniques are used for efficient document retrieval?",
        "How does the system handle semantic search across 500+ documents?",
        "What are the advantages of vector-based document indexing?",
        "Can you explain the document processing pipeline?"
    ];
    let currentSuggestionIndex = 0;

    // File type icons and handlers
    const fileTypes = {
        pdf: {
            icon: '📄',
            extensions: ['.pdf'],
            handler: handlePDFFile
        },
        word: {
            icon: '📝',
            extensions: ['.docx', '.doc'],
            handler: handleWordFile
        },
        excel: {
            icon: '📊',
            extensions: ['.xlsx', '.xls'],
            handler: handleExcelFile
        },
        image: {
            icon: '🖼️',
            extensions: ['.png', '.jpg', '.jpeg', '.gif'],
            handler: handleImageFile
        },
        video: {
            icon: '🎥',
            extensions: ['.mp4', '.webm'],
            handler: handleVideoFile
        },
        text: {
            icon: '📝',
            extensions: ['.txt'],
            handler: handleTextFile
        }
    };

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

    // Document List Management
    async function loadExistingDocuments() {
        try {
            const response = await fetch('http://127.0.0.1:5001/api/pfizer-files');
            const data = await response.json();
            if (data.success && data.files) {
                documents = data.files;
                hasDocuments = documents.length > 0;
                updateDocumentList();
            }
        } catch (error) {
            console.error('Error loading documents:', error);
            showError('Failed to load existing documents');
        }
    }

    function updateDocumentList() {
        documentList.innerHTML = '';
        
        if (!hasDocuments) {
            documentList.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-file-upload"></i>
                    <p>Upload PDF files to get started</p>
                </div>
            `;
            return;
        }

        documents.forEach(doc => {
            const docElement = document.createElement('div');
            docElement.className = `document-item ${currentDocument === doc ? 'active' : ''}`;
            docElement.innerHTML = `
                <div class="doc-title">${doc}</div>
                <div class="doc-info">PDF Document</div>
            `;
            docElement.addEventListener('click', () => loadDocument(doc));
            documentList.appendChild(docElement);
        });

        updateChatStatus();
    }

    // Document Upload and Processing
    async function handleFileSelect(event) {
        const files = Array.from(event.target.files);
        if (files.length === 0) return;
        
        await processFiles(files);
        event.target.value = ''; // Reset input
    }

    async function handleFolderSelect(event) {
        const files = Array.from(event.target.files);
        if (files.length === 0) return;
        
        await processFiles(files);
        event.target.value = ''; // Reset input
    }

    async function processFiles(files) {
        if (processingFiles) return;
        processingFiles = true;
        
        showUploadProgress();
        const totalFiles = files.length;
        let processedFiles = 0;
        
        try {
            for (const file of files) {
                const extension = '.' + file.name.split('.').pop().toLowerCase();
                const fileType = getFileType(extension);
                
                if (fileType) {
                    const formData = new FormData();
                    formData.append('file', file);
                    
                    try {
                        const response = await fetch('/upload', {
                            method: 'POST',
                            body: formData
                        });
                        
                        if (response.ok) {
                            const result = await response.json();
                            const document = {
                                id: result.id,
                                name: file.name,
                                type: fileType,
                                path: result.path,
                                size: formatFileSize(file.size),
                                uploadDate: new Date().toLocaleString()
                            };
                            
                            documents.push(document);
                            updateDocumentsList();
                        } else {
                            console.error(`Failed to upload ${file.name}`);
                        }
                    } catch (error) {
                        console.error(`Error uploading ${file.name}:`, error);
                    }
                }
                
                processedFiles++;
                updateProgress(processedFiles / totalFiles * 100);
            }
        } finally {
            processingFiles = false;
            hideUploadProgress();
        }
    }

    // UI Updates
    function updateProgress(percent) {
        progressBar.style.width = `${percent}%`;
        progressText.textContent = `Processing files... ${Math.round(percent)}%`;
    }

    function showUploadProgress() {
        uploadProgress.classList.remove('hidden');
        progressBar.style.width = '0%';
    }

    function hideUploadProgress() {
        setTimeout(() => {
            uploadProgress.classList.add('hidden');
        }, 1000);
    }

    function updateDocumentsList() {
        const filteredDocs = filterDocumentsList();
        
        if (filteredDocs.length === 0) {
            documentsContainer.innerHTML = `
                <div class="empty-state">
                    <p>No documents found</p>
                    <p class="supported-formats">Supported formats: PDF, DOCX, XLSX, PNG, JPG, MP4, MP3, TXT</p>
                </div>
            `;
            return;
        }
        
        documentsContainer.innerHTML = filteredDocs.map((doc, index) => `
            <div class="document-item ${index === currentDocumentIndex ? 'active' : ''}" 
                 onclick="selectDocument(${index})">
                <span class="document-icon">${doc.type.icon}</span>
                <div class="document-info">
                    <div class="document-name">${doc.name}</div>
                    <div class="document-meta">${doc.size} • ${doc.uploadDate}</div>
                </div>
            </div>
        `).join('');
    }

    // Document Handling
    function selectDocument(index) {
        currentDocumentIndex = index;
        const document = documents[index];
        updateDocumentsList();
        
        currentDocument.textContent = document.name;
        document.type.handler(document);
    }

    async function handlePDFFile(document) {
        try {
            const response = await fetch(`/view/${document.id}`);
            if (response.ok) {
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                
                viewerContent.innerHTML = `
                    <iframe src="${url}" style="width: 100%; height: 100%; border: none;"></iframe>
                `;
                
                // Enable navigation controls
                updateNavigationControls(true);
            }
        } catch (error) {
            console.error('Error loading PDF:', error);
            showError('Failed to load PDF');
        }
    }

    function handleWordFile(document) {
        viewerContent.innerHTML = `
            <div class="document-preview">
                <iframe src="https://view.officeapps.live.com/op/embed.aspx?src=${encodeURIComponent(document.path)}" 
                        style="width: 100%; height: 100%; border: none;"></iframe>
            </div>
        `;
        updateNavigationControls(false);
    }

    function handleExcelFile(document) {
        viewerContent.innerHTML = `
            <div class="document-preview">
                <iframe src="https://view.officeapps.live.com/op/embed.aspx?src=${encodeURIComponent(document.path)}" 
                        style="width: 100%; height: 100%; border: none;"></iframe>
            </div>
        `;
        updateNavigationControls(false);
    }

    function handleImageFile(document) {
        viewerContent.innerHTML = `
            <div class="image-preview" style="transform: scale(${zoomLevel})">
                <img src="${document.path}" alt="${document.name}">
            </div>
        `;
        updateNavigationControls(false);
    }

    function handleVideoFile(document) {
        viewerContent.innerHTML = `
            <div class="video-preview">
                <video controls>
                    <source src="${document.path}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
        `;
        updateNavigationControls(false);
    }

    function handleTextFile(document) {
        fetch(document.path)
            .then(response => response.text())
            .then(content => {
                viewerContent.innerHTML = `
                    <div class="text-preview">
                        <pre>${content}</pre>
                    </div>
                `;
            })
            .catch(error => {
                console.error('Error loading text file:', error);
                showError('Failed to load text file');
            });
        updateNavigationControls(false);
    }

    // Utility Functions
    function getFileType(extension) {
        for (const [type, config] of Object.entries(fileTypes)) {
            if (config.extensions.includes(extension.toLowerCase())) {
                return config;
            }
        }
        return null;
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`;
    }

    function filterDocumentsList() {
        const searchTerm = documentSearch.value.toLowerCase();
        const selectedType = fileTypeFilter.value;
        
        return documents.filter(doc => {
            const matchesSearch = doc.name.toLowerCase().includes(searchTerm);
            const matchesType = selectedType === 'all' || 
                               (selectedType === 'image' && doc.type.extensions.some(ext => ['.png', '.jpg', '.jpeg', '.gif'].includes(ext))) ||
                               (selectedType === doc.type.extensions[0].substring(1));
            return matchesSearch && matchesType;
        });
    }

    function filterDocuments() {
        updateDocumentsList();
    }

    // Chat Functions
    function handleInputChange() {
        sendButton.disabled = !userInput.value.trim();
    }

    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;
        
        // Add user message
        appendMessage('user', message);
        userInput.value = '';
        sendButton.disabled = true;
        
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message,
                    documentId: currentDocumentIndex >= 0 ? documents[currentDocumentIndex].id : null
                })
            });
            
            if (response.ok) {
                const result = await response.json();
                appendMessage('assistant', result.response);
            } else {
                throw new Error('Failed to get response');
            }
        } catch (error) {
            console.error('Error sending message:', error);
            appendMessage('assistant', 'Sorry, I encountered an error processing your request.');
        }
    }

    function appendMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}-message`;
        messageDiv.textContent = content;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Navigation and Zoom Controls
    function updateNavigationControls(enabled) {
        prevPageBtn.disabled = !enabled;
        nextPageBtn.disabled = !enabled;
        pageInfo.textContent = enabled ? `Page ${currentPage} of ${totalPages}` : '';
    }

    function adjustZoom(delta) {
        zoomLevel = Math.max(0.1, Math.min(3, zoomLevel + delta));
        const preview = viewerContent.querySelector('.image-preview');
        if (preview) {
            preview.style.transform = `scale(${zoomLevel})`;
        }
    }

    // Error Handling
    function showError(message) {
        viewerContent.innerHTML = `
            <div class="error-message">
                <p>⚠️ ${message}</p>
            </div>
        `;
    }

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

    // Initialize the application
    init();
});
