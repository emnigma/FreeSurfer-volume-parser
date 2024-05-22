import Chart from 'chart.js/auto'

(async function () {
  const data = {
    labels: [
      'Parietal',
      'Frontal',
      'Hyppocampi',
      'Occipital',
      'Temporal',
    ],
    datasets: [{
      label: 'Volume signature (norm %)',
      data: [98, 66, 72, 57, 90],
      fill: true,
      backgroundColor: 'rgba(255, 99, 132, 0.2)',
      borderColor: 'rgb(255, 99, 132)',
      pointBackgroundColor: 'rgb(255, 99, 132)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgb(255, 99, 132)'
    }]
  };

  new Chart(
    document.getElementById('radar'),
    {
      type: 'radar',
      data: data,
      options: {
        elements: {
          line: {
            borderWidth: 3
          }
        },
        scales: {
          r: {
            angleLines: {
              display: false
            },
            suggestedMin: 40,
            suggestedMax: 100
          }
        },
        chartArea: { backgroundColor: 'red' },
      }
    }
  );
})();
