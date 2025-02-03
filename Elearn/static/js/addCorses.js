document.addEventListener("DOMContentLoaded", () => {
    let addButton = document.querySelector(".create_course2");
    let addTitle = document.querySelector(".add_title");
    let addSlogan = document.querySelector(".add_slogan");
    let fileInput = document.querySelector(".file-input");
    let boxContainer = document.querySelector(".box-container");

    function buildElement(event) {
        event.preventDefault();

        if (addTitle.value === '' || addSlogan.value === '' || !fileInput.files.length) {
            alert("You must fill all fields and select a file.");
            return;
        }

        let reader = new FileReader();
        reader.onload = function(e) {
            localStorage.setItem('addTitle', addTitle.value);
            localStorage.setItem('addSlogan', addSlogan.value);
            localStorage.setItem('fileInput', e.target.result);

            let divBox = document.createElement("div");
            let divThumb = document.createElement("div");
            let img = document.createElement("img");
            let span = document.createElement("span");
            let h3 = document.createElement("h3");
            let a = document.createElement("a");
            let button = document.createElement("button");

            img.setAttribute("src", e.target.result);
            divBox.setAttribute("class", "box");
            divThumb.setAttribute("class", "thumb");
            h3.setAttribute("class", "title");
            button.setAttribute("class", "delete");
            a.setAttribute("href", "playlist.html");

            h3.innerText = addTitle.value;
            span.innerText = "1 video"; // Dynamic video count
            a.innerText = "View Playlist";
            button.innerText = "Delete";

            divThumb.appendChild(img);
            divThumb.appendChild(span);
            divBox.appendChild(divThumb);
            divBox.appendChild(h3);
            divBox.appendChild(a);
            divBox.appendChild(button);

            boxContainer.appendChild(divBox);

            addTitle.value = '';
            addSlogan.value = '';
            fileInput.value = '';

            // Event delegation for delete button
            boxContainer.addEventListener("click", function(e) {
                if (e.target && e.target.matches("button.delete")) {
                    e.target.closest(".box").remove();
                }
            });
        };

        reader.onerror = function(error) {
            console.error('Error occurred while reading the file: ', error);
        };

        reader.readAsDataURL(fileInput.files[0]);
    }

    if (addButton) {
        addButton.addEventListener("click", buildElement);
    }
});
