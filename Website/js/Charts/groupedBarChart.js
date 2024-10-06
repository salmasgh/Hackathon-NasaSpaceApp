let myChart; 

function updateBarChart(chartData) {
    // Extract the values from chartData object
    const soilmoisture = chartData.soil_moisture;
    const albedo = chartData.albedo;
    const vegetation_water_content = chartData.vegetation_water_content;

    // Structure the datasets with appropriate labels and values
    const vizualizing_data = [
        {
            label: 'Soil Parameters',
            data: [soilmoisture, albedo, vegetation_water_content], // Wrapping the value in an array
            backgroundColor: 'rgba(75, 192, 192, 0.6)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }
    ];

    fetch('data/soilmoisture.json') // Path to the JSON file
        .then(response => response.json())
        .then(data => {
            // Destroy the previous chart instance if it exists
            if (myChart) {
                myChart.destroy();
                myChart = null; // Set the chart variable to null after destroying it
            }

            // Create the chart using the fetched data
            const config = {
                type: 'bar',
                data: {
                    labels: ['Soil Moisture', 'Albedo','Vegetation Water Content'], // Ensure you have the labels from the JSON
                    datasets: vizualizing_data // Datasets properly structured
                },
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            stacked: false, // Change to true if you want stacked bars
                        },
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Soil Moisture (%)' // Add a title to the Y-axis
                            }
                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: 'Soil Moisture Levels Across Regions (Grouped Bar Chart)' // Chart title
                        },
                        legend: {
                            position: 'top',
                        }
                    }
                }
            };

            // Get the context of the canvas element and create the chart
            const ctx = document.getElementById('groupedBarChart').getContext('2d');
            myChart = new Chart(ctx, config);  // Store the chart instance globally
        })
        .catch(error => console.error('Error loading JSON data:', error));
}

// Example usage with your chartData structure
const exampleData = {
    albedo: 0.049989645874999995,
    clay_fraction: 0.27589817625,
    organic_content: 12.945026125000002,
    sand_fraction: 0.37332762625,
    soil_moisture: 0.079465829125,
    vegetation_water_content: 0.6021020425000001
};

updateBarChart(exampleData);
