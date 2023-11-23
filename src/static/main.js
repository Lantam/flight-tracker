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
    const locationValue = formData.get('location');
    const formDataObject = {};
    formData.forEach((value, key) => {
        formDataObject[key] = value;
    });
    let zoomLevel = map.getZoom();
    let bounds = map.getBounds();

    fetch('', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ form_data: formDataObject, filter_value: locationValue, zoom_level: zoomLevel, bounds: bounds }),
    })
    .then(response => response.json())
    .then(data => {
        mapFunctions.updateMarkers(map, data.markers);
        addFilter(data.filters)
    })
    .catch(error => {
        console.log('Error: ', error);
        console.log('Response Text:', error.responseText);
    });
});


function addRemoveFilterListeners() {
    let removeFilterButtons = document.querySelectorAll('.remove-filter');
    removeFilterButtons.forEach(function (button) {
      button.addEventListener('click', function () {
        let filterValue = this.getAttribute('data-filter');
        console.log(filterValue)
        removeFilter(filterValue);
      });
    });
  }


function addFilter(filterValue) {
    let filterList = document.getElementById('filter-list');
    let newFilterItem = document.createElement('li');
    newFilterItem.innerHTML = `${filterValue}<button class="remove-filter" data-filter="${filterValue}">X</button>`;
    filterList.appendChild(newFilterItem);

    addRemoveFilterListeners();
}


function removeFilter(filterValue) {
    let filterList = document.getElementById('filter-list');
    let filterToRemove = document.querySelector(`[data-filter="${filterValue}"]`);
    let zoomLevel = map.getZoom();
    let bounds = map.getBounds();

    fetch('remove-filter', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ filter_value: filterValue, zoom_level: zoomLevel, bounds: bounds }),
    })
      .then(response => response.json())
      .then(data => {
        console.log('AJAX response:', data);
        if (data.status === 'success') {
            filterList.removeChild(filterToRemove.parentNode);
            mapFunctions.updateMarkers(map, data.markers)
        }
      })
      .catch(error => {
          console.error('Error:', error);
      });
}