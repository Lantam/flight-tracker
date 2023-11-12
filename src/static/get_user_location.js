export const successCallback = (position) => {
    console.log(position);
};

export const errorCallback = (error) => {
    console.log(error);
};

export const getCurrentLocation = (successCallback, errorCallback) => {
    navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
};