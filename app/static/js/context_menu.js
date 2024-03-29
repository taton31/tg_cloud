
function showContextMenu(event) {
    event.preventDefault();
    data = event.target.getAttribute('data');
    console.log(event.target.getAttribute('data'))
    const contextMenu = document.getElementById("userContextMenu");
    contextMenu.style.display = "block";
    contextMenu.style.left = `${event.clientX}px`;
    contextMenu.style.top = `${event.clientY + window.scrollY}px`;
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
            fetch('/rename?' + data + '&new_name=' + new_name)
            .then(() => {
                window.location.reload();
            })
            .catch(error => console.error('Ошибка:', error));
        }

    } else if (action === 2) {
        new_path = prompt("Новый путь:", "")
        if (new_path) {
            fetch('/move?' + data + '&new_path=' + new_path)
            .then(() => {
                window.location.reload();
            })
            .catch(error => console.error('Ошибка:', error));
        }

    } else if (action === 3) {
        userConfirmed = confirm("Точно хочешь удалить?");
        if (userConfirmed) {
            fetch('/remove?' + data)
            .then(() => {
                window.location.reload();
            })
            .catch(error => console.error('Ошибка:', error));
        }

    } else if (action === 4) {
        
        let task_id = getRandomInt()

        fetch('/downloadfile?' + data + '&task_id=' + task_id)
        .then(response => {
            const contentDisposition = response.headers.get('Content-Disposition');
            const filenameMatch = contentDisposition && contentDisposition.match(/filename="(.+)"/);
            const filename = filenameMatch ? filenameMatch[1] : 'example.txt';
            const filename_decode = decodeURIComponent(filename)
            return Promise.all([response.blob(), Promise.resolve(filename_decode)]);
        })
        .then(([blob, filename]) => {
            const downloadLink = document.createElement('a');
            downloadLink.href = window.URL.createObjectURL(blob);
            downloadLink.download = filename;

            document.body.appendChild(downloadLink);
            downloadLink.click();

            document.body.removeChild(downloadLink);
        })
        .catch(error => {
            console.error('Error during file download:', error);
        });


        create_event_listener(task_id);

    }
}

