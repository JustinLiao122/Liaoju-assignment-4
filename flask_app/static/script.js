let cosineChart;

document.addEventListener('DOMContentLoaded', function() {
    const inputField = document.getElementById('UserInput');

    function search() {
        const userQuery = inputField.value;

        fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: userQuery })
        })
        .then(response => response.json())
        .then(data => {
            const top5Results = data.top5_results;
            const cosineDoc = data.cosine_doc;
            displayResults(top5Results, cosineDoc);
            displayCosine(cosineDoc);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    function displayResults(results, cosineDoc) {
        const container = document.getElementById('results-container');
        
        container.innerHTML = '';
        
        results.forEach((result, index) => {
            
            const resultDiv = document.createElement('div');
            resultDiv.classList.add('result-box');
            
            const docNumber = cosineDoc[index][1];
            const similarity = cosineDoc[index][0].toFixed(4);
            
            resultDiv.innerHTML = `<strong>Document ${docNumber}:</strong> <br/>${result}<br/><strong>Similarity: ${similarity}</strong>`;
            
            
            container.appendChild(resultDiv);
        });
    }
    function displayCosine(cosineDoc) {
       
        const cosineValues = cosineDoc.map(item => item[0]);
        const docNumbers = cosineDoc.map(item => `Doc ${item[1]}`);
        
        if (cosineChart) {
            cosineChart.destroy();
        }
        
        const ctx = document.getElementById('cosineChart').getContext('2d');
        cosineChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: docNumbers, 
                datasets: [{
                    label: 'Cosine Similarity',
                    data: cosineValues, 
                    backgroundColor: 'rgba(75, 192, 192, 0.6)', 
                    borderColor: 'rgba(75, 192, 192, 1)', 
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                const docNumber = cosineDoc[tooltipItem.dataIndex][1];
                                const cosineValue = cosineDoc[tooltipItem.dataIndex][0].toFixed(4);
                                return `Doc ${docNumber}: Cosine Similarity = ${cosineValue}`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true 
                    }
                }
            }
        });
    }
    

    
    const searchButton = document.querySelector('.glowing-btn');
    searchButton.addEventListener('click', search);
});
