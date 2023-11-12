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
        map.eachLayer(function (layer) {
            if (layer instanceof L.Marker) {
                map.removeLayer(layer);
            }
        });

        for (let markerData of data) {
            L.marker([markerData['latitude'], markerData['longitude']]).addTo(map);
        }
    })
    .catch(error => {
        console.log('Error: ', error);
    });
});
