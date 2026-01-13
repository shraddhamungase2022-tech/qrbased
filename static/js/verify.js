// Verification Page JavaScript

let cameraStream = null;
let cameraActive = false;

function switchTab(tabName) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));

    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => btn.classList.remove('active'));

    // Show selected tab
    document.getElementById(tabName).classList.add('active');

    // Add active class to clicked button
    event.target.classList.add('active');

    // Stop camera if switching away
    if (tabName !== 'camera' && cameraActive) {
        stopCamera();
    }
}

function startCamera() {
    const video = document.getElementById('cameraVideo');
    const startBtn = document.getElementById('startScan');
    const stopBtn = document.getElementById('stopScan');

    navigator.mediaDevices.getUserMedia({ 
        video: { 
            facingMode: 'environment',
            width: { ideal: 1280 },
            height: { ideal: 720 }
        } 
    })
    .then(function(stream) {
        cameraStream = stream;
        video.srcObject = stream;
        video.style.display = 'block';
        cameraActive = true;

        startBtn.style.display = 'none';
        stopBtn.style.display = 'inline-block';

        // Start scanning for QR codes
        scanQRCode();
    })
    .catch(function(err) {
        alert('Unable to access camera: ' + err.message);
    });
}

function stopCamera() {
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
    }

    const video = document.getElementById('cameraVideo');
    const startBtn = document.getElementById('startScan');
    const stopBtn = document.getElementById('stopScan');

    video.style.display = 'none';
    cameraActive = false;

    startBtn.style.display = 'inline-block';
    stopBtn.style.display = 'none';
}

function scanQRCode() {
    const video = document.getElementById('cameraVideo');
    const canvas = document.getElementById('cameraCanvas');
    const ctx = canvas.getContext('2d');

    function scan() {
        if (!cameraActive) return;

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(imageData.data, imageData.width, imageData.height, {
            inversionAttempts: 'dontInvert',
        });

        if (code) {
            // QR code found
            displayQRResult(code.data);
            stopCamera();
        } else {
            // Continue scanning
            requestAnimationFrame(scan);
        }
    }

    scan();
}

function displayQRResult(data) {
    const resultDiv = document.getElementById('scanResult');

    // Send data to backend for verification
    fetch('{% url "verify_api" %}', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: 'qr_data=' + encodeURIComponent(data)
    })
    .then(response => response.json())
    .then(result => {
        let html = `<div class="result-box ${result.status === 'valid' ? 'result-valid' : 'result-invalid'}">`;
        html += `<h3>${result.message}</h3>`;

        if (result.status === 'valid' && result.student) {
            html += '<div class="student-info">';
            html += `<div class="info-row"><span class="label">Name:</span><span class="value">${result.student.name}</span></div>`;
            html += `<div class="info-row"><span class="label">Roll Number:</span><span class="value">${result.student.roll_number}</span></div>`;
            html += `<div class="info-row"><span class="label">Department:</span><span class="value">${result.student.department}</span></div>`;
            html += `<div class="info-row"><span class="label">Year:</span><span class="value">${result.student.year}</span></div>`;
            if (result.student.photo) {
                html += `<div style="margin-top: 1rem;"><img src="${result.student.photo}" style="max-width: 150px; border-radius: 4px;"></div>`;
            }
            html += '</div>';
        }

        html += '</div>';
        resultDiv.innerHTML = html;
    })
    .catch(error => {
        resultDiv.innerHTML = `<div class="result-box result-invalid"><h3>❌ Error processing QR code</h3></div>`;
        console.error('Error:', error);
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    const startScanBtn = document.getElementById('startScan');
    const stopScanBtn = document.getElementById('stopScan');

    if (startScanBtn) {
        startScanBtn.addEventListener('click', startCamera);
    }

    if (stopScanBtn) {
        stopScanBtn.addEventListener('click', stopCamera);
    }

    // Set first tab as active on load
    const firstTab = document.querySelector('.tab-btn');
    if (firstTab) {
        firstTab.classList.add('active');
    }
});
