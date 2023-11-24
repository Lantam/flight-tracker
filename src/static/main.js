import { initializeMap, addMarkersOnZoomMove, getFilterElevation, getFilterBounds, updateMarkers } from './map.js';
import { getCurrentLocation, successCallback, errorCallback } from './get_user_location.js';
import { getCookie } from './cookie.js';
import { initializeFilterValues, getFilterValues, addFilterValue, addFilterButton } from './filter.js';


const csrftoken = getCookie('csrftoken');
const map = initializeMap();

getCurrentLocation(
    successCallback,
    errorCallback
);

addMarkersOnZoomMove(map, csrftoken);
initializeFilterValues(map);


document.getElementById('search-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const formValue = formData.get('location');

    const filterValues = getFilterValues();
    filterValues.push(formValue);
    addFilterValue(filterValues);
    const updatedFilterValues = getFilterValues();

    const elevationFilterValue = getFilterElevation(map)
    const [southWestBounds, northEastBounds] = getFilterBounds(map);

    const params = new URLSearchParams({
        elevation__gte: elevationFilterValue,
        latitude__gte: southWestBounds.lat,
        latitude__lte: northEastBounds.lat,
        longitude__gte: southWestBounds.lng,
        longitude__lte: northEastBounds.lng,
    });

    if (updatedFilterValues.length > 0) {
        params.set('search', updatedFilterValues.join(','));
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
        addFilterButton(map, formValue);
    })
    .catch(error => {
        console.log('Error: ', error);
    });
});
