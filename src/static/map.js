import { getFilterValues } from './filter.js';
import { getCookie } from './cookie.js';


let mapInstance;

export const initializeMap = () => {
    if (!mapInstance) {
        mapInstance = L.map('map',{
            maxBounds: [[-90, -Infinity], [90, Infinity],],
            maxBoundsViscosity: 1.0,
        }).setView([0, 0], 2);

        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 18,
            minZoom: 2,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        }).addTo(mapInstance);
    }

    return mapInstance;
};


const createCustomIcon = (iconUrl, rotationAngle) => {
    return L.divIcon({
        className: 'custom-icon',
        iconSize: [35, 35],
        iconAnchor: [17.5, 17.5],
        html: `<img src="${iconUrl}" style="width: ${35}px; height: ${35}px; transform: rotate(${rotationAngle+60}deg);">`,
    })
};


export const updateMarkers = (map, data) => {
    map.eachLayer(function (layer) {
        if (layer instanceof L.Marker) {
            map.removeLayer(layer);
        }
    });

    const [southWestBounds, northEastBounds] = getFilterBounds(map);
    const multiplier = worldCounter(southWestBounds.lng);
    const counter = mapscounter(southWestBounds.lng, northEastBounds.lng);

    const createPopupContent = markerData => `
        Registration Number: ${markerData.registration_number}<br>
        Country Code: ${markerData.country_code}<br>
        Longitude: ${markerData.longitude}<br>
        Latitude: ${markerData.latitude}<br>
        Elevation: ${markerData.elevation}<br>
        Head Direction: ${markerData.head_direction}<br>
        Airline ICAO: ${markerData.airline_icao}<br>
        Aircraft ICAO: ${markerData.aircraft_icao}<br>
        Departure ICAO: ${markerData.departure_icao}<br>
        Arrival ICAO: ${markerData.arrival_icao}<br>
        Status: ${markerData.status}<br>
    `;

    const createAndAddMarker = (latitude, longitude, rotationAngle, markerData) => {
        const marker = L.marker([latitude, longitude], { icon: createCustomIcon('../media/plane.png', rotationAngle) });
        marker.bindPopup(createPopupContent(markerData));
        marker.addTo(map);
    };

    for (let markerData of data) {
        if (southWestBounds.lng < -180) {
            if (markerData.longitude > southWestBounds.lng && ((360 * -multiplier)+180) < northEastBounds.lng) {
                for (let i = 0; i < counter; i++) {
                    createAndAddMarker(markerData.latitude, markerData.longitude - (360 * (multiplier - i)), markerData.head_direction, markerData)
                }
            }
        }
        if (northEastBounds.lng > 180) {
            if (markerData.longitude < northEastBounds.lng && ((360 * multiplier)-180) < southWestBounds.lng) {
                for (let i = 0; i < counter; i++) {
                    createAndAddMarker(markerData.latitude, markerData.longitude + (360 * (multiplier + i)), markerData.head_direction, markerData)
                }
            }
        }
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


const specialRound = (num) => {
    if (num >= 0) {
      return Math.floor(num);
    } else {
      return -Math.ceil(num);
    }
};

function specialRound2(num) {
    if (num < 0) {
      num = -num
    }
    return Math.ceil(num);

}

function mapscounter(input1, input2) {
    return specialRound2((input2 - input1) / 360)
  }


function worldCounter(longitude) {
    let value = specialRound((Math.abs(longitude) + 180) / 360)
    if (longitude % 180 === 0 && longitude !== 0) {
      value -= 1
    }
    return value
};


export const addMarkersOnZoomMove = (map, loadInitially = false) => {
    const fetchData = () => {
        const csrftoken = getCookie('csrftoken');
        const filterValues = getFilterValues();
        const elevationFilterValue = getFilterElevation(map);
        const [southWestBounds, northEastBounds] = getFilterBounds(map);

        const params = new URLSearchParams({
            elevation__gte: elevationFilterValue,
            latitude__gte: southWestBounds.lat,
            latitude__lte: northEastBounds.lat,
            longitude__gte: -180,
            longitude__lte: 180,
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
            updateMarkers(map, data)
        })
        .catch(error => {
            console.log('Error: ', error);
        });
    };

    map.on('zoomend moveend', fetchData);

    if (loadInitially) {
        fetchData();
    }
};