function chooseFile() {
    document.getElementById('fileInput').click();
}

document.getElementById('fileInput').addEventListener('change', function() {
    let fileInput = document.getElementById('fileInput');
    let pathInput = document.getElementById('pathInput');

    if (fileInput.files.length > 0) {
        let file = fileInput.files[0];
        let path = pathInput.value;
        let file_size = file.size;
        let formData = new FormData();
        formData.append('file', file);

        let xhr = new XMLHttpRequest();
        let task_id = getRandomInt();
        xhr.open('POST', '/uploadfile/?path=' + path + '&task_id=' + task_id + '&size=' + file_size, true);
        create_event_listener(task_id)
        
        xhr.upload.onprogress = function(e) {
            if (e.lengthComputable) {
                var progressPercentage = (e.loaded / e.total) * 100;
                progressBar.value = progressPercentage;
            }
        };
        
        xhr.onload = function() {
            if (xhr.status >= 200 && xhr.status < 300) {
                window.location.reload();
            } else {
                console.error('Ошибка:', xhr.status);
            }
        };

        xhr.send(formData);
    }
});