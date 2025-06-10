"use strict";
console.log("Hallo Trip Detail!");
const map = L.map('map');
// OpenStreetMap-Tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);
L.tileLayer('https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png', {
    attribution: 'Map: © OpenSeaMap contributors',
}).addTo(map);
// GPX-Datei laden

new L.GPX(gpx, {
    async: true,
    marker_options: {
        startIconUrl: 'https://unpkg.com/leaflet-gpx@1.5.1/pin-icon-start.png',
        endIconUrl: 'https://unpkg.com/leaflet-gpx@1.5.1/pin-icon-end.png',
        shadowUrl: 'https://unpkg.com/leaflet-gpx@1.5.1/pin-shadow.png'
    }
}).on('loaded', function (e) {
    map.fitBounds(e.target.getBounds());
}).addTo(map);
