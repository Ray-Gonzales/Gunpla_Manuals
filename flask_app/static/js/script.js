const dropArea = document.getElementById("drop-area");
const fileList = document.getElementById("fileList");
const fileElem = document.getElementById("fileElem");

// Prevent default drag behaviors
dropArea.addEventListener("dragover", e => {
    e.preventDefault();
    dropArea.classList.add("dragging");
});

dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("dragging");
});

dropArea.addEventListener("drop", e => {
    e.preventDefault();
    dropArea.classList.remove("dragging");
    handleFiles(e.dataTransfer.files);
});

// Handle file input change event
fileElem.addEventListener("change", () => {
    handleFiles(fileElem.files);
});

function handleFiles(files) {
    if (!files.length) {
        fileList.innerHTML = "<li>No files selected.</li>";
    } else {
        const list = fileList.querySelector("ul") || document.createElement("ul");
        fileList.appendChild(list);
        for (let i = 0; i < files.length; i++) {
        const li = document.createElement("li");

        const img = document.createElement("img");
        img.src = URL.createObjectURL(files[i]);
        img.height = 30;
        img.onload = function() {
            URL.revokeObjectURL(this.src);
        };

        const fileName = document.createTextNode(files[i].name);
        li.appendChild(img);
        li.appendChild(fileName);
        list.appendChild(li);
        }
    }
}
function handleFiles(files) {
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append('ins_manual', files[i]);
    }
    fetch('/upload_file', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            console.log('Files uploaded successfully!');
        } else {
            throw new Error('Error uploading files.');
        }
    })
    .catch(error => {
        console.error(error);
    });

    // Update the file list
    const list = fileList.querySelector("ul") || document.createElement("ul");
    fileList.appendChild(list);
    for (let i = 0; i < files.length; i++) {
        const li = document.createElement("li");

        const img = document.createElement("img");
        img.src = URL.createObjectURL(files[i]);
        img.height = 60;
        img.onload = function() {
            URL.revokeObjectURL(this.src);
        };

        const fileName = document.createTextNode(files[i].name);
        li.appendChild(img);
        li.appendChild(fileName);
        list.appendChild(li);
    }
}
