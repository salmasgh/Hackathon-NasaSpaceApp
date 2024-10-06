let myPieChart; // Global variable for the chart instance

function updatePieChart(chartData) {
    // Extract the values for clay, sand, and organic content from chartData
    const clay_fraction = chartData.clay_fraction;
    const sand_fraction = chartData.sand_fraction;
    const organic_content = chartData.organic_content;

    // Structure the datasets with appropriate labels and values
    const vizualizing_data = [
        {
            label: 'Clay Fraction',
            data: [clay_fraction],
            backgroundColor: 'rgba(153, 102, 255, 0.6)',
            borderColor: 'rgba(153, 102, 255, 1)',
            borderWidth: 1
        },
        {
            label: 'Sand Fraction',
            data: [sand_fraction],
            backgroundColor: 'rgba(75, 192, 192, 0.6)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        },
        {
            label: 'Organic Content',
            data: [organic_content],
            backgroundColor: 'rgba(255, 159, 64, 0.6)',
            borderColor: 'rgba(255, 159, 64, 1)',
            borderWidth: 1
        }
    ];

    // Destroy the previous pie chart if it exists
    if (myPieChart) {
        myPieChart.destroy();
    }

    // Create the pie chart configuration
    const config = {
        type: 'pie',
        data: {
            labels: ['Clay Fraction', 'Sand Fraction', 'Organic Content'], // Labels for the chart
            datasets: [{
                label: 'Soil Composition',
                data: [clay_fraction, sand_fraction, organic_content], // Directly use the data values for the pie chart
                backgroundColor: [
                    'rgba(153, 102, 255, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(255, 159, 64, 0.6)'
                ],
                borderColor: [
                    'rgba(153, 102, 255, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Soil Composition Distribution'
                },
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            const percentage = tooltipItem.raw * 100;
                            return `${tooltipItem.label}: ${percentage.toFixed(2)}%`; // Format the tooltip to show percentage
                        }
                    }
                }
            }
        }
    };

    // Get the context of the canvas element and create the chart
    const ctx = document.getElementById('pieChart').getContext('2d');
    myPieChart = new Chart(ctx, config); // Store the pie chart instance globally
}

// Example chartData object
const exampleChartData = {
    clay_fraction: 0.24657121,
    sand_fraction: 0.05681554,
    organic_content: 0.31861073
};

// Call the function and pass the data
updatePieChart(exampleChartData);
