document.addEventListener("DOMContentLoaded", () => {
    let addButton = document.querySelector(".create_course2");
    let addTitle = document.querySelector(".add_title");
    let addSlagan = document.querySelector(".add_slagan");
    let fileInput = document.querySelector(".file-input");
    let thumb = document.querySelector(".thumb");
    let playlistHead = document.querySelector(".playlist_head");
    let playlistsPar = document.querySelector(".playlists_par");

    // Check if there are stored data in localStorage
    let title = localStorage.getItem('playlistTitle');
    let slogan = localStorage.getItem('playlistSlogan');
    let imageSrc = localStorage.getItem('playlistImage');

    // If there are stored data, populate the elements with them
    if (title && slogan && imageSrc) {
        playlistHead.innerText = title;
        playlistsPar.innerText = slogan;

        let thumbImg = document.createElement("img");
        thumbImg.setAttribute("src", imageSrc);
        thumb.appendChild(thumbImg);

        // Clear localStorage after use
        localStorage.removeItem('playlistTitle');
        localStorage.removeItem('playlistSlogan');
        localStorage.removeItem('playlistImage');
    }

    // Add event listener to the "Add" button
    addButton.addEventListener("click", () => {
        if (addTitle.value === '' || addSlagan.value === '') {
            alert("You must fill all fields.");
            return;
        }

        if (fileInput.files.length > 0) {
            let reader = new FileReader();
            reader.onload = () => {
                // Store the data in localStorage
                localStorage.setItem('playlistTitle', addTitle.value);
                localStorage.setItem('playlistSlogan', addSlagan.value);
                localStorage.setItem('playlistImage', reader.result);
                // Redirect to playlist.html
                window.location.href = 'playlist.html';
            };
            reader.readAsDataURL(fileInput.files[0]);
        } else {
            alert("Please select an image file.");
        }
    });
});