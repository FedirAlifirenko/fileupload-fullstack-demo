// Constants
const API_URL = 'http://localhost:8000/api';

// Initialize Resumable
const r = new Resumable({
    target: `${API_URL}/files/upload`,
    chunkSize: 1 * 1024 * 1024, // 1 MB
    simultaneousUploads: 3,
    testChunks: true,
    throttleProgressCallbacks: 1,
    headers: {
        'Authorization': getAuthHeader()
    }
});

// Event Handlers
r.on('fileAdded', file => r.upload());

r.on('fileProgress', file => console.log('File progress', file.progress()));

r.on('fileSuccess', (file, message) => {
    console.log('File uploaded successfully', file);
    completeUpload(file);
    fetchFileList();  // Refresh the list of files
});

r.on('fileError', (file, message) => console.error('File upload error', message));

// Add a file input to trigger the upload
document.getElementById('fileInput').addEventListener('change', event => {
    r.addFile(event.target.files[0]);
});

// Login form Auth header
document.getElementById('login-form').addEventListener('submit', event => {
    event.preventDefault();
    handleLogin();
});

// Logout button functionality
document.getElementById('logout-button').addEventListener('click', handleLogout);

// Handle Login
function handleLogin() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const authHeader = `Basic ${btoa(`${username}:${password}`)}`;

    localStorage.setItem('authHeader', authHeader);

    updateLoginState(username);
    console.log('auth header saved');
    fetchFileList();
}

// Handle Logout
function handleLogout() {
    localStorage.removeItem('authHeader');
    updateLoginState(null);
    console.log('auth header removed');
    clearFileList();
}

// Update Login State
function updateLoginState(username) {
    const userMessage = document.getElementById('user-login-message');
    const loginForm = document.getElementById('login-form');
    const logoutButton = document.getElementById('logout-button');

    if (username) {
        userMessage.textContent = `Logged in as ${username}`;
        loginForm.style.display = 'none';
        logoutButton.style.display = 'block';
    } else {
        userMessage.textContent = 'Not logged in yet.';
        loginForm.style.display = 'block';
        logoutButton.style.display = 'none';
    }
}

// Clear File List
function clearFileList() {
    const fileList = document.getElementById('files');
    const noFilesMessage = document.getElementById('no-files-message');
    fileList.innerHTML = ''; 
    noFilesMessage.style.display = 'block';
}

// Complete Upload
function completeUpload(file) {
    fetch(`${API_URL}/files/upload/complete`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': getAuthHeader(),
        },
        body: JSON.stringify({
            resumable_identifier: file.uniqueIdentifier,
            resumable_filename: file.fileName,
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to complete upload');
        }
        fetchFileList();
        return response.json();
    })
    .then(data => console.log('Upload complete:', data))
    .catch(error => console.error('Error completing upload:', error));
}

// Fetch File List
async function fetchFileList() {
    try {
        const response = await fetch(`${API_URL}/files`, {
            headers: {
                'Authorization': getAuthHeader(),
            },
        });
        if (!response.ok) {
            throw new Error('Failed to fetch file list');
        }
        const data = await response.json();
        updateFileList(data.files);
    } catch (error) {
        console.error('Error fetching file list:', error);
    }
}

// Update File List
function updateFileList(files) {
    const fileList = document.getElementById('files');
    const noFilesMessage = document.getElementById('no-files-message');
    fileList.innerHTML = ''; // Clear the list

    if (files.length === 0) {
        noFilesMessage.style.display = 'block';
    } else {
        noFilesMessage.style.display = 'none';
        files.forEach(file => {
            const row = document.createElement('tr');

            const fileNameCell = document.createElement('td');
            fileNameCell.textContent = file.name;
            row.appendChild(fileNameCell);

            const fileSizeCell = document.createElement('td');
            fileSizeCell.textContent = formatFileSize(file.size);
            row.appendChild(fileSizeCell);

            fileList.appendChild(row);
        });
    }
}

// Format File Size
function formatFileSize(bytes) {
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    if (bytes === 0) return '0 Byte';
    const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)), 10);
    return `${(bytes / Math.pow(1024, i)).toFixed(2)} ${sizes[i]}`;
}

// Get Auth Header
function getAuthHeader() {
    return localStorage.getItem('authHeader');
}

// Initialize on Page Load
window.onload = function() {
    const authHeader = getAuthHeader();
    if (authHeader) {
        const username = atob(authHeader.split(' ')[1]).split(':')[0];
        updateLoginState(username);
    } else {
        updateLoginState(null);
    }

    fetchFileList();
    document.getElementById('no-files-message').style.display = 'none';
};
