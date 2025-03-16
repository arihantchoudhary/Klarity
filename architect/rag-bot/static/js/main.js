document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const files = document.getElementById('fileInput').files;
    const status = document.getElementById('uploadStatus');
    
    for (let file of files) {
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            status.innerHTML += `<p>${file.name}: ${data.message || data.error}</p>`;
        } catch (error) {
            status.innerHTML += `<p>${file.name}: Upload failed</p>`;
        }
    }
});

document.getElementById('queryButton').addEventListener('click', async () => {
    const query = document.getElementById('queryInput').value;
    const responseDiv = document.getElementById('response');
    
    try {
        const response = await fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });
        const data = await response.json();
        responseDiv.innerHTML = `<p>${data.response || data.error}</p>`;
    } catch (error) {
        responseDiv.innerHTML = '<p>Error processing query</p>';
    }
});