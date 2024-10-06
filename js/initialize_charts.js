

fetch(`http://localhost:5000/api/data?bounding_box=${lowerLeftLon}&bounding_box=${lowerLeftLat}&bounding_box=${upperRightLon}&bounding_box=${upperRightLat}&start_date=${start_date}&end_date=${end_date}`)
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
