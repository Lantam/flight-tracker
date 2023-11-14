import * as mapFunctions from './map.js';
import * as geolocationFunctions from './get_user_location.js';
import * as cookieFunctions from './cookie.js';

const csrftoken = cookieFunctions.getCookie('csrftoken');
const map = mapFunctions.initializeMap();

geolocationFunctions.getCurrentLocation(
    geolocationFunctions.successCallback,
    geolocationFunctions.errorCallback
);

mapFunctions.addMarkersOnZoomMove(map, csrftoken);


document.getElementById('search-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const formData = new FormData(event.target);

    fetch('', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken,
        },
        body: new URLSearchParams(formData).toString(),
    })
    .then(response => response.json())
    .then(data => {
        mapFunctions.updateMarkers(map, data.markers);
    })
    .catch(error => {
        console.log('Error: ', error);
    });
});


document.getElementById('clear_filter').addEventListener('click', function (event) {
    event.preventDefault();

    let zoomLevel = map.getZoom();
    let bounds = map.getBounds();
    
    fetch('clear-filter', {
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
        mapFunctions.updateMarkers(map, data.markers);
    })
    .catch(error => {
        console.log('Error: ', error);
    });
});