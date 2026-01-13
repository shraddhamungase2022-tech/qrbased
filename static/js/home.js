// Home Page JavaScript

function showStudentModal() {
    document.getElementById('studentModal').style.display = 'block';
}

function closeStudentModal() {
    document.getElementById('studentModal').style.display = 'none';
}

function goToStudentId() {
    const studentId = document.getElementById('studentIdInput').value.trim();
    if (studentId) {
        window.location.href = `/student/${studentId}/`;
    } else {
        alert('Please enter a Student ID');
    }
}

// Allow Enter key in input
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('studentIdInput');
    if (input) {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                goToStudentId();
            }
        });
    }
});
