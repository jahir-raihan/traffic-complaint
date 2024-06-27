document.addEventListener('DOMContentLoaded', function () {
    // Function to handle file input changes and preview
    function handleFileChange(event) {
        const inputElement = event.target;
        const file = inputElement.files[0];

        if (file) {
            const reader = new FileReader();

            reader.onload = function (e) {
                // Logic to display the preview or process the file
                console.log(`File preview: ${e.target.result}`);
                // Additional code to handle the file preview can be added here
            };

            reader.readAsDataURL(file);
        }
    }

    // Select the main complaint file inputs
    const mainImageInput = document.getElementById('main-complaint-image');
    const mainVideoInput = document.getElementById('main-complaint-video');

    // Select the popup complaint file inputs
    const popupImageInput = document.getElementById('popup-complaint-image');
    const popupVideoInput = document.getElementById('popup-complaint-video');

    // Add event listeners to handle file changes
    mainImageInput.addEventListener('change', handleFileChange);
    mainVideoInput.addEventListener('change', handleFileChange);
    popupImageInput.addEventListener('change', handleFileChange);
    popupVideoInput.addEventListener('change', handleFileChange);

    // Function to toggle the attachment popup
    function toggleAttachPopup() {
        const popup = document.getElementById('attach-popup');
        if (popup) {
            popup.classList.toggle('hidden');
        }
    }

    // Add event listener to the attach button
    document.querySelector('.attach button').addEventListener('click', toggleAttachPopup);

    // Function to disable the modal and reset its contents
    function disableModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('hidden');
        }
        document.getElementById('header').classList.remove('blur-sm');
        document.getElementById('container').classList.remove('blur-sm');
        document.getElementById('footer').classList.remove('blur-sm');

        // Clear the file inputs in the modal
        document.getElementById('popup-complaint-image').value = '';
        document.getElementById('popup-complaint-video').value = '';
        
        // Clear the modal body content
        document.getElementById('modal-body').innerHTML = '';
    }

    // Function to enable the modal and apply blur to background
    function enableModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('hidden');
        }
        document.getElementById('header').classList.add('blur-sm');
        document.getElementById('container').classList.add('blur-sm');
        document.getElementById('footer').classList.add('blur-sm');
    }

    // Expose functions to be used in the HTML
    window.disableModal = disableModal;
    window.enableModal = enableModal;
    window.toggleAttachPopup = toggleAttachPopup;
});
