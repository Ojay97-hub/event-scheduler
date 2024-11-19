// Toggle button for viewing comments
const toggleButton = document.getElementById('toggleButton');
const commentsSection = document.getElementById('commentsSection');

// Listen for changes in the collapse component
commentsSection.addEventListener('show.bs.collapse', () => {
    toggleButton.textContent = 'Hide Comments'; // Change button text to "Hide Comments"
});

commentsSection.addEventListener('hide.bs.collapse', () => {
    toggleButton.textContent = 'View Comments'; // Change button text back to "View Comments"
});

// Max word count for comments
function checkWordCount(textareaId, wordCountId) {
    const textarea = document.getElementById(textareaId);
    const wordCount = document.getElementById(wordCountId);
    const words = textarea.value.trim().split(/\s+/);
    const wordLimit = 50;

    // Count words, handle empty input
    const currentWordCount = words.filter(word => word.length > 0).length;

    // Update the word count display
    wordCount.textContent = `${currentWordCount}/${wordLimit} words`;

    // Disable button if the word limit is exceeded
    const submitBtn = document.getElementById('commentSubmitBtn');
    if (currentWordCount > wordLimit) {
        wordCount.classList.add('text-danger');
        wordCount.textContent = `Limit exceeded! ${currentWordCount}/${wordLimit} words`;
        submitBtn.disabled = true;
    } else {
        wordCount.classList.remove('text-danger');
        submitBtn.disabled = false;
    }
}

// Toggle the reply form visibility
function toggleReplyForm(commentId) {
    const form = document.getElementById(`replyForm${commentId}`);
    form.classList.toggle('d-none');
}

// Show the inline edit form
function editComment(commentId) {
    const commentContent = document.getElementById(`commentContent${commentId}`);
    const editForm = document.getElementById(`editForm${commentId}`);

    // If the edit form doesn't exist, create it
    if (!editForm) {
        const form = document.createElement('div');
        form.id = `editForm${commentId}`;
        form.classList.add('d-none'); // Initially hidden

        // Create a textarea for editing the comment content
        const textarea = document.createElement('textarea');
        textarea.classList.add('form-control');
        textarea.rows = 2;
        textarea.textContent = commentContent.textContent.trim();
        form.appendChild(textarea);

        // Create Save button
        const saveButton = document.createElement('button');
        saveButton.classList.add('btn', 'btn-sm', 'btn-primary');
        saveButton.textContent = 'Save';
        saveButton.onclick = function (event) {
            submitEdit(event, commentId);
        };
        form.appendChild(saveButton);

        // Create Cancel button
        const cancelButton = document.createElement('button');
        cancelButton.classList.add('btn', 'btn-sm', 'btn-secondary');
        cancelButton.textContent = 'Cancel';
        cancelButton.onclick = function () {
            cancelEdit(commentId);
        };
        form.appendChild(cancelButton);

        // Append the form below the comment content
        commentContent.parentNode.appendChild(form);
    }

    // Hide the current comment content and show the edit form
    commentContent.classList.add('d-none');
    editForm.classList.remove('d-none');
}

// Submit edited comment via AJAX
function submitEdit(event, commentId) {
    event.preventDefault();

    const content = document.querySelector(`#editForm${commentId} textarea`).value.trim();
    if (!content) {
        alert('Content cannot be empty!');
        return;
    }

    fetch(`/edit_comment/${commentId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: JSON.stringify({ content })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById(`commentContent${commentId}`).textContent = content;
                document.getElementById(`commentContent${commentId}`).classList.remove('d-none');
                document.getElementById(`editForm${commentId}`).classList.add('d-none');
            } else {
                alert(data.error || 'Error updating the comment');
            }
        })
        .catch(() => alert('An error occurred'));
}

// Cancel editing a comment
function cancelEdit(commentId) {
    document.getElementById(`editForm${commentId}`).classList.add('d-none');
    document.getElementById(`commentContent${commentId}`).classList.remove('d-none');
}

// Delete a comment via AJAX
function deleteComment(commentId) {
    fetch(`/delete_comment/${commentId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById(`comment${commentId}`).remove();
            } else {
                alert(data.error || 'Error deleting the comment');
            }
        })
        .catch(() => alert('An error occurred'));
}

// Add event listeners for edit links
document.querySelectorAll('.edit-comment-link').forEach(link => {
    link.addEventListener('click', event => {
        event.preventDefault();
        const commentId = link.getAttribute('data-comment-id');
        editComment(commentId);
    });
});

// Add event listeners for delete links
document.querySelectorAll('.delete-comment-link').forEach(link => {
    link.addEventListener('click', event => {
        event.preventDefault();
        const commentId = link.getAttribute('data-comment-id');
        deleteComment(commentId);
    });
});

// Add event listeners for reply form toggles
document.querySelectorAll('.edit-comment-link').forEach(link => {
    link.addEventListener('click', event => {
        event.preventDefault();
        const commentId = link.getAttribute('data-comment-id');
        toggleReplyForm(commentId);
    });
});