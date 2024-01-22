progressBar = document.getElementById('progressBar');

function getRandomInt() {
    return Math.floor(Math.random() * 100000);
  }


function create_event_listener(task_id){
    const evtSource = new EventSource('/load_progress?' + 'task_id=' + task_id);

    evtSource.onmessage = function(event) {
        console.log(event.data);
        progressBar.value = event.data;
        if (event.data==100){
            evtSource.close();

        }
    };
    
    evtSource.onerror = function(err) {
        console.error("EventSource failed:", err);
        evtSource.close();
    };
}