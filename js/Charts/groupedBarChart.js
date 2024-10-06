fetch('data/soilmoisture.json') // Path to the JSON file
                  .then(response => response.json())
                  .then(data => {
                     // Create the chart using the fetched data
                        const config = {
                            type: 'bar',
                            data: data,
                            options: {
                                responsive: true,
                                scales: {
                                    x: {
                                        stacked: false,
                                    },
                                    y: {
                                        beginAtZero: true
                                    }
                                },
                                plugins: {
                                    title: {
                                        display: true,
                                        text: 'Soil Moisture Levels Across Regions (Grouped Bar Chart)'
                                    }
                                }
                            }
                        };
                     // Get the context of the canvas element and create the chart
                        const ctx = document.getElementById('groupedBarChart').getContext('2d');
                        const myChart = new Chart(ctx, config);
                    })
                    .catch(error => console.error('Error loading JSON data:', error));