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
const gpx = '{{ trip.gpx_file.url }}'; // URL der GPX-Datei
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
// GPX-Download Control hinzufügen
const GPXDownloadControl = L.Control.extend({
    onAdd: function (map) {
        const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');
        container.style.backgroundColor = 'white';
        container.style.padding = '2px 6px';
        container.style.cursor = 'pointer';
        container.style.fontSize = '14px';
        container.style.lineHeight = '1.2';
        container.style.borderRadius = '4px';
        container.title = "GPX-Datei herunterladen";
        container.innerHTML = `<a href="{{ trip.gpx_file.url }}" download style="color: #007bff; text-decoration: none;">
<i class="fas fa-download"></i> GPX Download
</a>`;
        // Verhindert, dass Klicks auf das Control die Karte verschieben
        L.DomEvent.disableClickPropagation(container);
        return container;
    },
    onRemove: function (map) {
        // Nichts nötig hier
    }
});
// Control unten rechts hinzufügen (Position 'bottomright')
map.addControl(new GPXDownloadControl({ position: 'bottomright' }));
// Vollbild-Button Logik
const fullscreenBtn = document.getElementById('fullscreenBtn');
const mapDiv = document.getElementById('map');
fullscreenBtn.addEventListener('click', () => {
    if (!document.fullscreenElement) {
        mapDiv.requestFullscreen().catch(err => alert(`Fehler beim Vollbild: ${err.message}`));
    }
    else {
        document.exitFullscreen();
    }
});
// Karte bei Vollbildänderung neu rendern
document.addEventListener('fullscreenchange', () => {
    map.invalidateSize();
    if (document.fullscreenElement) {
        // Wenn Vollbild aktiv: auf GPX-Track zoomen und zentrieren
        // if (polyline) {
        //     map.fitBounds(polyline.getBounds());
        // }
    }
});
