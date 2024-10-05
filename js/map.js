var map;
var marker1, marker2;
var square;
var points = [];
var isDrawing = false;

// Function to enable drawing mode
function enableDrawSquareMode() {
    points = [];
    isDrawing = false; 
    document.getElementById('draw-button').disabled = true; // Disable button during selection
    if(marker1) {
        map.removeLayer(marker1);
    }
    if(marker2) {
        map.removeLayer(marker2);
    }
}

// Function to draw a temporary square while dragging the mouse
function drawTemporarySquare(startPoint, currentPoint) {
    var southWest = [Math.min(startPoint.lat, currentPoint.lat), Math.min(startPoint.lng, currentPoint.lng)];
    var northEast = [Math.max(startPoint.lat, currentPoint.lat), Math.max(startPoint.lng, currentPoint.lng)];

    if (square) {
        map.removeLayer(square);
    }
    if(marker2) {
        map.removeLayer(marker2);
    }

    square = L.rectangle([southWest, northEast], { color: 'blue', weight: 1 }).addTo(map);
}

// Function to finalize the square and display diagonal coordinates
function finalizeSquare() {
    if (points.length === 2) {
        var southWest = [Math.min(points[0].lat, points[1].lat), Math.min(points[0].lng, points[1].lng)];
        var northEast = [Math.max(points[0].lat, points[1].lat), Math.max(points[0].lng, points[1].lng)];

        if (square) {
            map.removeLayer(square);
        }

        square = L.rectangle([southWest, northEast], { color: 'blue', weight: 1 }).addTo(map);

        document.getElementById('diagonal').innerText =
            `Diagonal: SW (${southWest[0].toFixed(5)}, ${southWest[1].toFixed(5)}) - NE (${northEast[0].toFixed(5)}, ${northEast[1].toFixed(5)})`;

        points = []; // Reset the points array
        isDrawing = false; // Reset drawing state
        document.getElementById('draw-button').disabled = false; // Re-enable button
    }
}

// Initialize the map
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
        var lat = position.coords.latitude;
        var lng = position.coords.longitude;

        document.getElementById('coordinates').innerText = `Latitude: ${lat}, Longitude: ${lng}`;

        map = L.map('map').setView([lat, lng], 13);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap'
        }).addTo(map);

        // On mouse down, place the first marker
        map.on('mousedown', function(e) {
            if (points.length < 2) {
                points.push({ lat: e.latlng.lat, lng: e.latlng.lng });

                if (points.length === 1) {
                    if (marker1) {
                        map.removeLayer(marker1);
                    }
                    if(marker2) {
                        map.removeLayer(marker2);
                    }
                    if(square) {
                        map.removeLayer(square);
                    }
                    marker1 = L.circleMarker([points[0].lat, points[0].lng], {
                        color: 'red',
                        radius: 5
                    }).addTo(map);
                    isDrawing = true; // Start drawing mode
                } else if (points.length === 2) {
                    if (marker2) {
                        map.removeLayer(marker2);
                    }
                    marker2 = L.circleMarker([points[1].lat, points[1].lng], {
                        color: 'red',
                        radius: 5
                    }).addTo(map);
                    finalizeSquare(); // Finalize square after placing second marker
                }
            }
        });

        // Draw a temporary square while moving the mouse
        map.on('mousemove', function(e) {
            if (isDrawing && points.length === 1) {
                drawTemporarySquare(points[0], { lat: e.latlng.lat, lng: e.latlng.lng });
            }
        });
    }, function() {
        alert("Geolocation failed.");
    });
} else {
    alert("Geolocation is not supported by your browser.");
}
