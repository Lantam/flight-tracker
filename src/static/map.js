export const initializeMap = () => {
    const map = L.map('map').setView([0, 0], 2);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        minZoom: 2,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    return map;
};

export const addMarkersOnZoomMove = (map, csrftoken) => {
    map.on('zoomend moveend', function () {
        let zoomLevel = map.getZoom();
        let bounds = map.getBounds();

        console.log(zoomLevel);
        console.log(bounds);

        fetch('get_zoom_level_bounds', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ zoom_level: zoomLevel, bounds: bounds }),
        })
            .then(response => response.json())
            .then(data => {
                map.eachLayer(function (layer) {
                    if (layer instanceof L.Marker) {
                        map.removeLayer(layer);
                    }
                });
                for (let dat of data) {
                    console.log(dat);
                    L.marker([dat['latitude'], dat['longitude']]).addTo(map);
                }
            })
            .catch(error => {
                console.log('Error: ', error);
            });
    });
};