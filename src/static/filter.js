import { getFilterElevation, getFilterBounds, updateMarkers } from './map.js';
import { getCookie } from './cookie.js';


export const getFilterValues = () => {
    return JSON.parse(localStorage.getItem('filterValues')) || [];
};


export const addFilterValue = (values) => {
    const currentValues = getFilterValues();
    const updatedValues = [...currentValues, ...values];
    localStorage.setItem('filterValues', JSON.stringify(updatedValues));
};


export const initializeFilterValues = (map) => {
    const storedFilterValues = getFilterValues();
    const filterList = document.getElementById('filter-list');

    storedFilterValues.forEach(filterValue => {
        const newFilterItem = createFilterButton(filterValue);
        filterList.appendChild(newFilterItem);
    });

    addRemoveFilterListeners(map);
};


export const addRemoveFilterListeners = (map) => {
    let removeFilterButtons = document.querySelectorAll('.remove-filter');
    removeFilterButtons.forEach(function (button) {
      button.addEventListener('click', function () {
        let filterValue = this.getAttribute('data-filter');
        removeFilter(map, filterValue);
      });
    });
};


export const createFilterButton = (filterValue) => {
    const newFilterItem = document.createElement('li');
    newFilterItem.innerHTML = `${filterValue}<button class="remove-filter" data-filter="${filterValue}">X</button>`;
    return newFilterItem;
};


export const addFilterButton = (map, filterValue) => {
    const filterList = document.getElementById('filter-list');
    const newFilterItem = createFilterButton(filterValue);
    filterList.appendChild(newFilterItem);

    addRemoveFilterListeners(map);
};


export const removeFilter = (map, filterValue) => {
    const csrftoken = getCookie('csrftoken');

    let filterList = document.getElementById('filter-list');
    let filterToRemove = document.querySelector(`[data-filter="${filterValue}"]`);

    const filterValues = getFilterValues();
    const updatedFilterValues = filterValues.filter(value => value !== filterValue);
    localStorage.setItem('filterValues', JSON.stringify(updatedFilterValues));

    const elevationFilterValue = getFilterElevation(map);
    const [southWestBounds, northEastBounds] = getFilterBounds(map);

    const params = new URLSearchParams({
        elevation__gte: elevationFilterValue,
        latitude__gte: southWestBounds.lat,
        latitude__lte: northEastBounds.lat,
        longitude__gte: southWestBounds.lng,
        longitude__lte: northEastBounds.lng,
    });

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
        filterList.removeChild(filterToRemove.parentNode);
        updateMarkers(map, data)
    })
    .catch(error => {
        console.error('Error:', error);
    });
};
