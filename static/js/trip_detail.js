"use strict";
console.log("Hallo Trip Detail!");

function drawMap() {
    const map = L.map('map');
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    L.tileLayer('https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png', {
        attribution: 'Map: © OpenSeaMap contributors',
    }).addTo(map);

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
}

function drawBearingsHistogram() {
    const ctx = document.getElementById('bearings_histogram');

    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['N', 'NNO', 'NO', 'ONO', 'O', 'OSO', 'SO', 'SSO', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'],
            datasets: [{
                label: 'Kurse und ihre Anteil am Gesamttörn',
                data: course_histogram,
                borderWidth: 1
            }]
        },
        options: {
            r: {
                beginAtZero: true,
                ticks: {
                    callback: function (value, index, ticks) {
                        return (value * 100) + '%';
                    }
                }
            }
        }
    });
}


drawMap()
drawBearingsHistogram()