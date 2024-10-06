// fetch('data/xxxx.json')  // Path to the JSON file
//             .then(response => response.json())
//             .then(data => {
//                 // Create the pie chart using the fetched data
//                 const config = {
//                     type: 'pie',
//                     data: {
//                         labels: data.labels,  // Labels for the pie chart
//                         datasets: data.datasets  // Datasets for the pie chart
//                     },
//                     options: {
//                         responsive: true,
//                         plugins: {
//                             title: {
//                                 display: true,
//                                 text: 'XXXXXXXXX'
//                             },
//                             legend: {
//                                 position: 'top',
//                             },
//                             tooltip: {
//                                 callbacks: {
//                                     label: function(tooltipItem) {
//                                         return `${tooltipItem.label}: ${tooltipItem.raw}%`;
//                                     }
//                                 }
//                             }
//                         }
//                     }
//                 };

//                 // Get the context of the canvas element and create the chart
//                 const ctx = document.getElementById('XXXXXX').getContext('2d');
//                 const myPieChart = new Chart(ctx, config);
//             })
//             .catch(error => console.error('Error loading JSON data:', error));