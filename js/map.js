var map;
var marker1, marker2;
var square;
var points = [];
var isDrawing = false;

// Initialize the map
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
        var lat = position.coords.latitude;
        var lng = position.coords.longitude;

        document.getElementById('coordinates').innerText = `Latitude: ${lat}, Longitude: ${lng}`;

        map = L.map('map').setView([lat, lng], 13);

        // Use Esri World Imagery (satellite) tiles
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            maxZoom: 19,
            attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
        }).addTo(map);

        // Handle map click to select points
        map.on('click', function(e) {
            handleMapClick(e.latlng);
        });

        // Draw a temporary square while moving the mouse
        map.on('mousemove', function(e) {
            if (isDrawing && points.length === 1) {
                drawTemporarySquare(points[0], e.latlng);
            }
        });

    }, function() {
        alert("Geolocation failed.");
    });
} else {
    alert("Geolocation is not supported by your browser.");
}

// Handle map click event to place markers and finalize the square
function handleMapClick(latlng) {
    if (points.length < 2) {
        points.push(latlng);

        if (points.length === 1) {
            placeMarker1(latlng);
            isDrawing = true;
        } else if (points.length === 2) {
            placeMarker2(latlng);
            finalizeSquare();
        }
    }
}

// Place the first marker
function placeMarker1(latlng) {
    if (marker1) {
        map.removeLayer(marker1);
    }
    if(marker2){
        map.removeLayer(marker2);
    }
    if(square){ 
        map.removeLayer(square);
    }
    marker1 = L.circleMarker(latlng, { color: 'red', radius: 5 }).addTo(map);
}

// Place the second marker
function placeMarker2(latlng) {
    if (marker2) {
        map.removeLayer(marker2);
    }
    marker2 = L.circleMarker(latlng, { color: 'red', radius: 5 }).addTo(map);
}

// Draw a temporary square
function drawTemporarySquare(startPoint, currentPoint) {
    var southWest = [Math.min(startPoint.lat, currentPoint.lat), Math.min(startPoint.lng, currentPoint.lng)];
    var northEast = [Math.max(startPoint.lat, currentPoint.lat), Math.max(startPoint.lng, currentPoint.lng)];

    if (square) {
        map.removeLayer(square);
    }

    square = L.rectangle([southWest, northEast], { color: 'blue', weight: 1 }).addTo(map);
}

// Finalize the square and display diagonal coordinates
// Finalize the square and display diagonal coordinates
function finalizeSquare() {
    if (points.length === 2) {
        // Calculate lower left and upper right coordinates
        var lowerLeftLat = Math.min(points[0].lat, points[1].lat);
        var lowerLeftLon = Math.min(points[0].lng, points[1].lng);
        var upperRightLat = Math.max(points[0].lat, points[1].lat);
        var upperRightLon = Math.max(points[0].lng, points[1].lng);

        if (square) {
            map.removeLayer(square);
        }

        // Create rectangle with lower left and upper right coordinates
        square = L.rectangle([[lowerLeftLat, lowerLeftLon], [upperRightLat, upperRightLon]], { color: 'blue', weight: 1 }).addTo(map);

        // Display the diagonal coordinates
        document.getElementById('diagonal').innerText =
            `Diagonal: SW (${lowerLeftLat.toFixed(5)}, ${lowerLeftLon.toFixed(5)}) - NE (${upperRightLat.toFixed(5)}, ${upperRightLon.toFixed(5)})`;

        // Fetch data from the API
        console.log("fetching data");
        fetch(`http://localhost:5000/api/data?bounding_box=${lowerLeftLon}&bounding_box=${lowerLeftLat}&bounding_box=${upperRightLon}&bounding_box=${upperRightLat}`)
            .then(response => {
                console.log(response);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Process the data and update the UI as needed
                console.log(data); // For debugging, you can remove this later

                // Example: Display the data in a div
                document.getElementById('data-display').innerText = JSON.stringify(data, null, 2);
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            })
            
            ;

        // Reset state
        points = [];
        isDrawing = false;
        document.getElementById('draw-button').disabled = false;
    }
}


// Enable drawing mode
function enableDrawSquareMode() {
    points = [];
    isDrawing = false;
    document.getElementById('draw-button').disabled = true;

    if (marker1) {
        map.removeLayer(marker1);
    }
    if (marker2) {
        map.removeLayer(marker2);
    }
    if (square) {
        map.removeLayer(square);
    }
}