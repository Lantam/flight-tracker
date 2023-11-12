let map = L.map('map').setView([0, 0], 2);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom: 18, minZoom: 2, attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'}).addTo(map);


map.on('zoomend moveend', function () {
    let zoomLevel = map.getZoom();
    let bounds = map.getBounds();

    fetch('/api/get_zoom_level_and_bounds/', {
        method: 'POST',
        headers: {'Conten-Type': 'application/json'},
        body: JSON.stringify({zoomLevel, bounds}),
    }).then(response => response.json()).catch(error => {console.log('Fehler bei der Anfrage: ', error)});

    fetch('/api/send_data_to_frontend/', {
        method: 'GET',
        headers: {'Conten-Type': 'application/json'},
    }).then(response => response.json()).catch(error => {console.log('Fehler bei der Anfrage: ', error)});
});




