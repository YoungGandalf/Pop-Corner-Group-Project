let map;

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 39.2550, lng: -76.7076 },
        zoom: 15,
    });
}