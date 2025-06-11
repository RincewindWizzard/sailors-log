"use strict";
console.log("Hallo Trip Detail!");

const data = JSON.parse(document.getElementById('trip-data').textContent);
console.log(data);

function drawMap() {
    const map = L.map('map');
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    L.tileLayer('https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png', {
        attribution: 'Map: © OpenSeaMap contributors',
    }).addTo(map);

    new L.GPX(data.gpx, {
        async: true,
        marker_options: {
            startIconUrl: 'https://unpkg.com/leaflet-gpx@1.5.1/pin-icon-start.png',
            endIconUrl: 'https://unpkg.com/leaflet-gpx@1.5.1/pin-icon-end.png',
            shadowUrl: 'https://unpkg.com/leaflet-gpx@1.5.1/pin-shadow.png'
        }
    }).on('loaded', function (e) {
        map.fitBounds(e.target.getBounds());
    }).addTo(map);


    // Vollbild-Button Logik
    const fullscreenBtn = document.getElementById('fullscreenBtn');
    const mapDiv = document.getElementById('map');

    fullscreenBtn.addEventListener('click', () => {
        if (!document.fullscreenElement) {
            mapDiv.requestFullscreen().catch(err => alert(`Fehler beim Vollbild: ${err.message}`));
        } else {
            document.exitFullscreen();
        }
    });

    // Karte bei Vollbildänderung neu rendern
    document.addEventListener('fullscreenchange', () => {
        map.invalidateSize();

        if (document.fullscreenElement) {
            // Wenn Vollbild aktiv: auf GPX-Track zoomen und zentrieren
            if (polyline) {
                map.fitBounds(polyline.getBounds());
            }
        }
    });

}

function drawBearingsHistogram() {
    const ctx = document.getElementById('bearings_histogram');
    const labels = ['N', 'NNO', 'NO', 'ONO', 'O', 'OSO', 'SO', 'SSO', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'];
    const dataValues = labels.map(label => data.bearing_histogram[label] || 0);
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['N', 'NNO', 'NO', 'ONO', 'O', 'OSO', 'SO', 'SSO', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'],
            datasets: [{
                label: 'Kurse und ihre Anteil am Gesamttörn',
                data: dataValues,
                borderWidth: 1
            }]
        },

        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false // 👈 Legende deaktivieren
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    min: 0,
                    ticks: {
                        //stepSize: 0.2,
                        callback: function (value) {
                            return (value * 100) + '%';
                        }
                    }
                }
            }
        }
    });
}


function drawWindCourseHistogram() {
    const ctx = document.getElementById('wind_course_histogram');
    const wind_course_histogram = data.wind_course_histogram;

    if (wind_course_histogram) {
        console.log(wind_course_histogram);


        var labels = ["Toter Winkel", "Hart am Wind", "Am Wind", "Halbwind", "Raumschots", "Vorwind"];
        labels = labels.concat(labels.slice(1, -1).reverse());
        const dataValues = [
            wind_course_histogram.NO_GO_ZONE,
            wind_course_histogram.CLOSE_HAULED_STARBOARD,
            wind_course_histogram.HAULED_STARBOARD,
            wind_course_histogram.BEAM_REACH_STARBOARD,
            wind_course_histogram.BROAD_REACH_STARBOARD,
            wind_course_histogram.RUNNING,
            wind_course_histogram.BROAD_REACH_PORT,
            wind_course_histogram.BEAM_REACH_PORT,
            wind_course_histogram.HAULED_PORT,
            wind_course_histogram.CLOSE_HAULED_PORT
        ];

        new Chart(ctx, {
            type: 'radar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Prozentualer Anteil der Windkurse zum Gesamttörn',
                    data: dataValues,
                    borderWidth: 1,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    pointBackgroundColor: 'rgba(54, 162, 235, 1)'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false // 👈 Legende deaktivieren
                    }
                },
                scales: {
                    r: {
                        beginAtZero: true,
                        min: 0,
                        ticks: {
                            //stepSize: 0.2,
                            callback: function (value) {
                                return (value * 100) + '%';
                            }
                        }
                    }
                }
            }
        });
    }
}

function drawSpeedGraph() {
    const ctx = document.getElementById('speed_graph');

    const speed_graph = data.speed_graph.map(entry => ({
        x: entry.time,
        y: entry.speed
    }));

    new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Geschwindigkeit',
                data: speed_graph,
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'minute',
                        displayFormats: {
                            minute: 'HH:mm'   // <-- hier im 'time' Objekt!
                        },
                        tooltipFormat: 'HH:mm:ss'
                    },
                    title: {
                        display: true,
                        text: 'Zeit'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Geschwindigkeit in Knoten'
                    }
                }
            },
        }
    });
}


drawMap()
drawBearingsHistogram()
drawSpeedGraph()
drawWindCourseHistogram()