
function showContextMenu(event) {
    event.preventDefault();
    data = event.target.getAttribute('data');
    console.log(event.target.getAttribute('data'))
    const contextMenu = document.getElementById("userContextMenu");
    contextMenu.style.display = "block";
    contextMenu.style.left = `${event.clientX}px`;
    contextMenu.style.top = `${event.clientY}px`;
    document.addEventListener("click", hideContextMenu);
}

function hideContextMenu() {
    const contextMenu = document.getElementById("userContextMenu");
    contextMenu.style.display = "none";
    document.removeEventListener("click", hideContextMenu);
}

function handleContextAction(action) {
    console.log(data);
    hideContextMenu();
    if (action === 1) {
        new_name = prompt("Новое название:", "")
        if (new_name) {
            fetch('/rename?' + data + '&new_name=' + new_name).then(window.location.reload())
        }

    } else if (action === 2) {
        new_path = prompt("Новый путь:", "")
        if (new_path) {
            fetch('/move?' + data + '&new_path=' + new_path).then(window.location.reload())
        }

    } else if (action === 3) {
        userConfirmed = confirm("Точно хочешь удалить?");
        if (userConfirmed) {
            fetch('/remove?' + data).then(window.location.reload())
        }

    } else if (action === 4) {
        
        let task_id = getRandomInt()

        fetch('/downloadfile?' + data + '&task_id=' + task_id)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const contentDisposition = response.headers.get('content-disposition');
            const filenameMatch = contentDisposition && contentDisposition.match(/filename="(.+)"/);
            const filename = filenameMatch ? filenameMatch[1] : 'downloaded-file.txt';
            const filename_decode = decodeURIComponent(filename)

            const contentLength = parseInt(response.headers.get('content-length'), 10);
            let loadedBytes = 0;

            const downloadLink = document.createElement('a');

            downloadLink.download = filename_decode;
            document.body.appendChild(downloadLink);

            const reader = response.body.getReader();
            
            

            parts = []
            function read() {
                return reader.read().then(({ value, done }) => {
                    if (done) {
                        blob = new Blob(parts);
                        downloadLink.href = window.URL.createObjectURL(blob);
                        downloadLink.click();
                        document.body.removeChild(downloadLink);
                        return;
                    }

                    loadedBytes += value.byteLength;
                    const progress = (loadedBytes / contentLength) * 100;
                    progressBar.value = progress;
                    
                    parts.push(value)
                    read();
                });
            }

            read();
            
        })
        .catch(error => console.error('Error during download:', error));


        create_event_listener(task_id);

    }
}

