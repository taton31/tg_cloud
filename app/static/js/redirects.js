function redirectToDetails(path_to) {
    window.location.href = `/?path=${path_to}`;
}

function redirectToSearch() {
    window.location.href = `/search`;
}

function create_folder(path) {
    new_name = prompt("Введите имя:", "")
    if (new_name) {
        fetch('/create?' + 'name=' + new_name + '&path=' + path).then(window.location.reload())
    }
}