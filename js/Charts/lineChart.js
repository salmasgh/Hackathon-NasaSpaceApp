fetch('data/soilmoisture.json')  // Path to the JSON file
            .then(response => response.json())
            .then(data => {
                // Create the line chart using the fetched data
                const config = {
                    type: 'line',
                    data: data,
                    options: {
                        responsive: true,
                        plugins: {
                            title: {
                                display: true,
                                text: 'Soil Moisture Levels Over Time (Line Chart)'
                            },
                            tooltip: {
                                mode: 'index',
                                intersect: false
                            }
                        },
                        interaction: {
                            mode: 'nearest',
                            axis: 'x',
                            intersect: false
                        },
                        scales: {
                            x: {
                                display: true,
                                title: {
                                    display: true,
                                    text: 'Months'
                                }
                            },
                            y: {
                                display: true,
                                title: {
                                    display: true,
                                    text: 'Soil Moisture (%)'
                                },
                                beginAtZero: true
                            }
                        }
                    }
                };

                // Get the context of the canvas element and create the chart
                const ctx = document.getElementById('lineChart').getContext('2d');
                const myLineChart = new Chart(ctx, config);
            })
            .catch(error => console.error('Error loading JSON data:', error));