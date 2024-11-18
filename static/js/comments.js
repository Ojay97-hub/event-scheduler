    // JavaScript to toggle button text
    const toggleButton = document.getElementById('toggleButton');
    const commentsSection = document.getElementById('commentsSection');

    // Listen for changes in the collapse component
    commentsSection.addEventListener('show.bs.collapse', function () {
        toggleButton.textContent = 'Hide Comments'; // Change button text to "Hide Comments"
    });

    commentsSection.addEventListener('hide.bs.collapse', function () {
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
        if (currentWordCount > wordLimit) {
            wordCount.classList.add('text-danger');
            wordCount.textContent = `Limit exceeded! ${currentWordCount}/${wordLimit} words`;
            document.getElementById(`${textareaId}SubmitBtn`).disabled = true;
        } else {
            wordCount.classList.remove('text-danger');
            document.getElementById(`${textareaId}SubmitBtn`).disabled = false;
        }
    }
    
    // Toggle the reply form visibility
    function toggleReplyForm(commentId) {
            const form = document.getElementById(`replyForm${commentId}`);
            form.classList.toggle('d-none');
    }
    
    // Function to show the inline edit form
    function editComment(commentId) {
        // Show the edit form and hide the current comment content
        document.getElementById('editForm' + commentId).classList.remove('d-none');
        document.getElementById('commentContent' + commentId).classList.add('d-none');
    }

    // Function to handle form submission (AJAX)
    function submitEdit(event, commentId) {
        event.preventDefault();  // Prevent form submission
    
        var newContent = document.querySelector(`#editForm${commentId} textarea`).value.trim();
        if (!newContent) {
            alert('Content cannot be empty!');
            return;
        }
    
        // Send the new content to the server via AJAX
        fetch(`/edit_comment/${commentId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify({
                content: newContent,
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update the comment content on success
                document.getElementById('commentContent' + commentId).textContent = newContent;
                document.getElementById('commentContent' + commentId).classList.remove('d-none');
                document.getElementById('editForm' + commentId).classList.add('d-none');
            } else {
                alert('Error updating the comment');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred');
        });
    }
    

    // Function to cancel the edit and restore the original comment
    function cancelEdit(commentId) {
        document.getElementById('editForm' + commentId).classList.add('d-none');
        document.getElementById('commentContent' + commentId).classList.remove('d-none');
    }

    // Function to delete the comment directly without confirmation
    function deleteComment(commentId) {
        // Make an AJAX request to delete the comment
        fetch(`/delete_comment/${commentId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remove the comment from the page directly
                document.getElementById('comment' + commentId).remove();
            } else {
                alert('Error deleting the comment');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred');
        });
    }
