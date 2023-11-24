import { getFilterValues } from './filter.js';
import { getCookie } from './cookie.js';


let mapInstance;

export const initializeMap = () => {
    if (!mapInstance) {
        mapInstance = L.map('map').setView([0, 0], 2);
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 18,
            minZoom: 2,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(mapInstance);
    }

    return mapInstance;
};


export const updateMarkers = (map, data) => {
    map.eachLayer(function (layer) {
        if (layer instanceof L.Marker) {
            map.removeLayer(layer);
        }
    });

    for (let markerData of data) {
        L.marker([markerData.latitude, markerData.longitude]).addTo(map);
    }
};


export const getFilterElevation = (map) => {
    const elevation_mapping = {
        1: 14000,
        2: 14000,
        3: 13500,
        4: 13000,
        5: 12000,
        6: 10000,
        7: 9000,
    };
    const zoomLevel = map.getZoom();
    const elevationFilterValue = elevation_mapping[zoomLevel] || 0;
    return elevationFilterValue
};


export const getFilterBounds = (map) => {
    const bounds = map.getBounds();
    const southWestBounds = bounds.getSouthWest();
    const northEastBounds = bounds.getNorthEast();
    return [southWestBounds, northEastBounds]
};


export const addMarkersOnZoomMove = (map) => {
    map.on('zoomend moveend', function () {
        const csrftoken = getCookie('csrftoken');
        const filterValues = getFilterValues();
        const elevationFilterValue = getFilterElevation(map);
        const [southWestBounds, northEastBounds] = getFilterBounds(map);

        const params = new URLSearchParams({
            elevation__gte: elevationFilterValue,
            latitude__gte: southWestBounds.lat,
            latitude__lte: northEastBounds.lat,
            longitude__gte: southWestBounds.lng,
            longitude__lte: northEastBounds.lng,
        });

        if (filterValues.length > 0) {
            params.set('search', filterValues.join(','));
        }
    
        let url = `api/api/?${params.toString()}`;

        fetch(url, {
            method: 'GET',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken,
            },
        })
        .then(response => response.json())
        .then(data => {
            updateMarkers(map, data);
        })
        .catch(error => {
            console.log('Error: ', error);
        });
    });
};