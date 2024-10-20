// Constants
const API_URL = 'http://localhost:8000/api/files';

var r = new Resumable({
    target: API_URL + '/upload',
    chunkSize: 1 * 1024 * 1024, // 1 MB
    simultaneousUploads: 3,
    testChunks: true,
    throttleProgressCallbacks: 1,
});

// Event handlers
r.on('fileAdded', function(file) {
    r.upload();
});

r.on('fileProgress', function(file) {
    console.log('File progress', file.progress());
});

r.on('fileSuccess', function(file, message) {
    console.log('File uploaded successfully', file);
    completeUpload(file);
});

r.on('fileError', function(file, message) {
    console.error('File upload error', message);
});

// Add a file input to trigger the upload
document.getElementById('fileInput').addEventListener('change', function(event) {
    r.addFile(event.target.files[0]);
});

function completeUpload(file) {
    fetch(API_URL + '/upload/complete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
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
        return response.json();
    })
    .then(data => {
        console.log('Upload complete:', data);
    })
    .catch(error => {
        console.error('Error completing upload:', error);
    });
}
