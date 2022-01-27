const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['2011', '2012', '2013', '2014', '2015', '2016'],
        datasets: [{
            label: '# of Votes',
            data: [8, 12, 19, 3, 5, 2, 3],
            backgroundColor: [ 
				'rgba(255, 255,255, 0.2)',
                'rgba(0, 158, 158, 0.2)', //заполнение
                'rgba(0, 158, 158, 0.2)',
                'rgba(0, 158, 158, 0.2)',
                'rgba(0, 158, 158, 0.2)',
                'rgba(0, 158, 158, 0.2)',
                'rgba(0, 158, 158, 0.2)'
            ],
            borderColor: [ //цвета точек
                'rgba(150, 25, 15, 1)', //линия и 1 точка
				'rgba(0, 0, 255, 1)',
				'rgba(0, 0, 255, 1)', 
                'rgba(0, 0, 255, 1)', 
                'rgba(0, 0, 255, 1)',
                'rgba(0, 0, 255, 1)',
                'rgba(0, 0, 255, 1)',
                'rgba(0, 0, 255, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});


//--------------------------------------------------------------------------------



