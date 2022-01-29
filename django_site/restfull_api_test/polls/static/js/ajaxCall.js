

function createChart1(label, dataset, dataset2){
    // var ctx = document.getElementById('myChart').getContext('2d');
    // $("canvas#myChart").remove();
    // $("div.chartjs-size-monitor").remove();
    // $("div.graphic").append('<canvas id="myChart" class="chart1 chartjs-render-monitor" height="70"></canvas>');
    var ctx = document.getElementById('myChart').getContext('2d');
    myChart.destroy()
    myChart = new Chart(ctx, {
        type: 'line',
        data: {														
            labels: label,
            datasets: dataset,
            },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }				
    });

    // var ctx2 = document.getElementById('myChart2').getContext('2d');
    // $("canvas#myChart2").remove();
    // $("div.chartjs-size-monitor").remove();
    // $("div.graphic").append('<canvas id="myChart2" class="chart2 chartjs-render-monitor" height="70"></canvas>');
    var ctx2 = document.getElementById('myChart2').getContext('2d');
    myChart2.destroy()
    myChart2 = new Chart(ctx2, {
        type: 'line',
        data: {														
            labels: label,
            datasets: dataset2,
            },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }				
    })
};

$(document).ready(function(){
    $(".dropdown-select").on('change', function(){
        $.ajax({
            url: '',
            type: 'get',
            data: {
                selected_station: $('option:selected', this).text()
            },
            success: function(response){
                $(".stationName").text(response.name)
                console.log(response.name)
                if (response.name == "Station_0020CF3B")
                {                    
                    var dates = response['dates']
                    var air_temp = response['air_temp_avg']
                    var soil_temp = response['soil_temp_avg']
                    var humidity = response['relative_humidity_avg']
                    var soil_moisture = response['soil_moisture']                    
                    
                    tableParent = document.getElementById('myTable').parentNode
                    $("#myTable").remove()
                    tableChild = document.createElement('table')
                    tableChild.id = 'myTable'
                    tableChild.classList.add('table')
                    var newRow = tableChild.insertRow(0);
                    newRow.insertCell(0).outerHTML = '<th onclick="sortTable(0)">Дата </th>';
                    newRow.insertCell(1).outerHTML = '<th onclick="sortTable(1)">Средняя температура воздуха, °C</th>';
                    newRow.insertCell(2).outerHTML = '<th onclick="sortTable(2)">Относительная влажность воздуха, %</th>';
                    newRow.insertCell(3).outerHTML = '<th onclick="sortTable(3)">Средняя температура почвы, °C</th>';
                    newRow.insertCell(4).outerHTML = '<th onclick="sortTable(4)">Влажность почвы, %</th>';
                    tableChild.appendChild(newRow);
                    for (var i in dates)
                    {
                        var newRow = tableChild.insertRow(i.indexOf);
                        newRow.insertCell(0).innerHTML = dates[i];
                        newRow.insertCell(1).innerHTML = air_temp[i];
                        newRow.insertCell(2).innerHTML = soil_temp[i];
                        newRow.insertCell(3).innerHTML = humidity[i];
                        newRow.insertCell(4).innerHTML = soil_moisture[i];            
                        tableChild.appendChild(newRow);           
                    }

                    tableParent.appendChild(tableChild)

                    $("#myTable tbody").remove()
                    $('#myTable tr:has(td)').wrapAll('<tbody></tbody>')
                    $("#myTable tbody").prependTo("#myTable")
                    $('#myTable tr:has(th)').wrapAll('<thead></thead>')
                    $("#myTable thead").prependTo("#myTable")
                    
                    var S_0020CF3B_dataset_temp = 
                    [
                        {                     
                            label: 'Средняя температура воздуха, °C',
                            data: air_temp,
                            backgroundColor: ['rgba(255, 255,255, 0.2)'],
                            borderColor: ['rgba(200, 0, 15, 1)'],
                            borderWidth: 2
                        },
                        {
                            label: 'Средняя температура почвы, °C',
                            data: soil_temp,
                            backgroundColor: ['rgba(255, 255, 255, 0.2)'],
                            borderColor: ['rgba(9, 132, 0, 1)'],                            
                            borderWidth: 2
                        }
                    ]

                    var S_0020CF3B_dataset_water = 
                    [
                        {                     
                            label: 'Относительная влажность воздуха, %',
                            data: humidity,
                            backgroundColor: ['rgba(255, 255,255, 0.2)'],
                            borderColor: ['rgba(200, 0, 15, 1)'],
                            borderWidth: 2
                        },
                        {
                            label: 'Средняя влажность почвы, %',
                            data: soil_moisture,
                            backgroundColor: ['rgba(255, 255, 255, 0.2)'],
                            borderColor: ['rgba(9, 132, 0, 1)'],                            
                            borderWidth: 2
                        }
                    ]

                    createChart1(dates, S_0020CF3B_dataset_temp, S_0020CF3B_dataset_water);
                   // createChart2(dates, S_0020CF3B_dataset_water);
                }

                if (response.name == "Station_002099C5")
                {                    
                    var dates = response['dates']
                    var air_temp = response['air_temp_avg']
                    var humidity = response['relative_humidity_avg']
                    var soil_temp_1 = response['soil_temp_1']
                    var soil_temp_2 = response['soil_temp_2']
                    var soil_temp_3 = response['soil_temp_3']

                    tableParent = document.getElementById('myTable').parentNode
                    $("#myTable").remove()
                    tableChild = document.createElement('table')
                    tableChild.id = 'myTable'
                    tableChild.classList.add('table')
                    var newRow = tableChild.insertRow(0);
                    newRow.insertCell(0).outerHTML = '<th onclick="sortTable(0)">Дата </th>';
                    newRow.insertCell(1).outerHTML = '<th onclick="sortTable(1)">Средняя температура воздуха, °C</th>';
                    newRow.insertCell(2).outerHTML = '<th onclick="sortTable(2)">Относительная влажность воздуха, %</th>';
                    newRow.insertCell(3).outerHTML = '<th onclick="sortTable(3)">Средняя температура почвы 1, °C</th>';
                    newRow.insertCell(4).outerHTML = '<th onclick="sortTable(4)">Средняя температура почвы 2, °C</th>';
                    newRow.insertCell(5).outerHTML = '<th onclick="sortTable(5)">Средняя температура почвы 3, °C</th>';
                    tableChild.appendChild(newRow);
                    for (var i in dates)
                    {
                        var newRow = tableChild.insertRow(i.indexOf);
                        newRow.insertCell(0).innerHTML = dates[i];
                        newRow.insertCell(1).innerHTML = air_temp[i];
                        newRow.insertCell(2).innerHTML = humidity[i];
                        newRow.insertCell(3).innerHTML = soil_temp_1[i];
                        newRow.insertCell(4).innerHTML = soil_temp_2[i];    
                        newRow.insertCell(5).innerHTML = soil_temp_3[i];            
                        tableChild.appendChild(newRow);           
                    }

                    tableParent.appendChild(tableChild)
                    
                    $("#myTable tbody").remove()
                    $('#myTable tr:has(td)').wrapAll('<tbody></tbody>')
                    $("#myTable tbody").prependTo("#myTable")
                    $('#myTable tr:has(th)').wrapAll('<thead></thead>')
                    $("#myTable thead").prependTo("#myTable")
                    

                    var S_002099C5_dataset = 
                    [
                        {                     
                            label: 'Средняя температура воздуха, °C',
                            data: air_temp,
                            backgroundColor: ['rgba(255, 255,255, 0.2)'],
                            borderColor: ['rgba(200, 0, 15, 1)'],
                            borderWidth: 2
                        },
                        {
                            label: 'Относительная влажность воздуха, %',
                            data: humidity,
                            backgroundColor: ['rgba(255, 255, 255, 0.2)'],
                            borderColor: ['rgba(9, 132, 0, 1)'],                            
                            borderWidth: 2
                        }
                    ]

                    var S_002099C5_dataset_temp = 
                    [
                        {                     
                            label: 'Температура почвы 1, °C',
                            data: soil_temp_1,
                            backgroundColor: ['rgba(255, 255,255, 0.2)'],
                            borderColor: ['rgba(200, 0, 15, 1)'],
                            borderWidth: 2
                        },
                        {
                            label: 'Температура почвы 2, °C',
                            data: soil_temp_2,
                            backgroundColor: ['rgba(255, 255, 255, 0.2)'],
                            borderColor: ['rgba(9, 132, 0, 1)'],                            
                            borderWidth: 2
                        },
                        {
                            label: 'Температура почвы 3, °C',
                            data: soil_temp_3,
                            backgroundColor: ['rgba(255, 255, 255, 0.2)'],
                            borderColor: ['rgba(9, 0, 243, 1)'],                            
                            borderWidth: 2
                        }
                    ]

                    createChart1(dates, S_002099C5_dataset, S_002099C5_dataset_temp);
                   // createChart2(dates, S_002099C5_dataset_temp);
                }

                
                // myChart = new Chart(ctx, {
                //     type: 'line',
                //     data: {														
                //         labels: info_dates,
                //         datasets: [
                //             {
                //                 label: 'Средняя температура воздуха, °C',
                //                 data: info_air_temp,
                //                 backgroundColor: ['rgba(255, 255,255, 0.2)'],
                //                 borderColor: ['rgba(200, 0, 15, 1)'],
                //                 borderWidth: 2
                //             },						
                //             {
                //                 label: 'Средняя температура почвы, °C',
                //                 data: info_soil_temp,
                //                 backgroundColor: ['rgba(255, 255, 255, 0.2)'],
                //                 borderColor: ['rgba(9, 132, 0, 1)'],
                                
                //                 borderWidth: 2
                //             },	
                //         ]
                //             },
                //     options: {
                //         scales: {
                //             y: {
                //                 beginAtZero: true
                //             }
                //         }
                //     }				
                // });					
		// 		  var ctx2 = document.getElementById('myChart2').getContext('2d');
		// 		  var myChart2 = new Chart(ctx2, {
		// 			  type: 'line',
		// 			  data: {														
		// 				  labels: [							  
		// 					  '2021-10-13 06:00:00',
		// 					  '2021-10-13 07:00:00',
		// 					  '2021-10-13 08:00:00',
		// 					  '2021-10-13 09:00:00',
		// 					  '2021-10-13 10:00:00',
		// 					  '2021-10-13 11:00:00',
		// 					  '2021-10-13 12:00:00',
		// 					  '2021-10-13 13:00:00',
		// 					  '2021-10-13 14:00:00',
		// 					  '2021-10-13 15:00:00',
		// 					  '2021-10-13 16:00:00',
		// 					  '2021-10-13 17:00:00',
		// 					  '2021-10-13 18:00:00',
		// 					  '2021-10-13 19:00:00',
		// 					  '2021-10-13 20:00:00',
		// 					  '2021-10-13 21:00:00',
		// 					  '2021-10-13 22:00:00',
		// 					  '2021-10-13 23:00:00',
		// 					  '2021-10-14 00:00:00',
		// 					  '2021-10-14 01:00:00',
		// 					  '2021-10-14 02:00:00',
		// 					  '2021-10-14 03:00:00',
		// 					  '2021-10-14 04:00:00',
		// 					  '2021-10-14 05:00:00',
		// 					  '2021-10-14 06:00:00',
		// 					  '2021-10-14 07:00:00',
		// 					  '2021-10-14 08:00:00',
		// 					  '2021-10-14 09:00:00',
		// 					  '2021-10-14 10:00:00',
		// 					  '2021-10-14 11:00:00',
		// 					  '2021-10-14 12:00:00',
		// 					  '2021-10-14 13:00:00',
		// 					  '2021-10-14 14:00:00',
		// 					  '2021-10-14 15:00:00',
		// 					  '2021-10-14 16:00:00',
		// 					  '2021-10-14 17:00:00',
		// 					  '2021-10-14 18:00:00',
		// 					  '2021-10-14 19:00:00',
		// 					  '2021-10-14 20:00:00',
		// 					  '2021-10-14 21:00:00',
		// 					  '2021-10-14 22:00:00',
		// 					  '2021-10-14 23:00:00',
		// 					  '2021-10-15 00:00:00',
		// 					  '2021-10-15 01:00:00',
		// 					  '2021-10-15 02:00:00',
		// 					  '2021-10-15 03:00:00',
		// 					  '2021-10-15 04:00:00',
		// 					  '2021-10-15 05:00:00',
		// 					  '2021-10-15 06:00:00',
		// 					  '2021-10-15 07:00:00',
		// 				  ],
		// 				  datasets: [
		// 					  {
		// 						  label: 'Относительная влажность воздуха, %',
		// 						  data: [
									  
		// 							  90.18,
		// 							  88.35,
		// 							  78.07,
		// 							  75.55,
		// 							  75.35,
		// 							  76.80,
		// 							  80.85,
		// 							  81.96,
		// 							  82.28,
		// 							  85.02,
		// 							  86.71,
		// 							  88.61,
		// 							  91.78,
		// 							  99.53,
		// 							  99.99,
		// 							  99.98,
		// 							  99.98,
		// 							  99.98,
		// 							  99.98,
		// 							  99.98,
		// 							  99.97,
		// 							  99.97,
		// 							  99.16,
		// 							  95.25,
		// 							  90.61,
		// 							  89.52,
		// 							  87.02,
		// 							  85.68,
		// 							  85.18,
		// 							  87.22,
		// 							  86.96,
		// 							  88.28,
		// 							  89.26,
		// 							  93.47,
		// 							  95.92,
		// 							  97.82,
		// 							  98.56,
		// 							  97.97,
		// 							  98.69,
		// 							  99.95,
		// 							  99.99,
		// 							  99.99,
		// 							  100.00,
		// 							  100.00,
		// 							  98.86,
		// 							  94.78,
		// 							  86.48,
		// 							  78.94,
		// 							  71.69,
		// 							  63.78,
		// 						  ],
		// 						  backgroundColor: ['rgba(255, 255, 255, 0.2)'],
		// 						  borderColor: ['rgba(200, 0, 15, 1)'],
		// 						  borderWidth: 2
		// 					  },						
		// 					  {
		// 						  label: 'Средняя влажность почвы, %',
		// 						  data: [
									  
		// 							  17.97,
		// 							  18.76,
		// 							  19.14,
		// 							  19.02,
		// 							  18.91,
		// 							  18.83,
		// 							  18.76,
		// 							  18.71,
		// 							  18.65,
		// 							  18.59,
		// 							  18.54,
		// 							  18.50,
		// 							  18.46,
		// 							  18.42,
		// 							  18.38,
		// 							  18.36,
		// 							  18.35,
		// 							  18.31,
		// 							  18.28,
		// 							  18.24,
		// 							  18.21,
		// 							  18.17,
		// 							  18.13,
		// 							  18.08,
		// 							  18.04,
		// 							  17.99,
		// 							  17.95,
		// 							  17.89,
		// 							  17.86,
		// 							  17.82,
		// 							  17.77,
		// 							  17.76,
		// 							  17.73,
		// 							  17.71,
		// 							  17.66,
		// 							  17.54,
		// 							  17.40,
		// 							  17.21,
		// 							  17.00,
		// 							  16.81,
		// 							  16.60,
		// 							  16.37,
		// 							  16.16,
		// 							  15.92,
		// 							  15.71,
		// 							  15.62,
		// 							  15.68,
		// 							  16.00,
		// 							  16.41,
		// 							  16.54,
		// 						  ],
		// 						  backgroundColor: ['rgba(255, 255, 255, 0.2)'],
		// 						  borderColor: ['rgba(9, 132, 0, 1)'],
		// 						  borderWidth: 2
		// 					  },		
		// 				  ]
		// 					  },
		// 			  options: {
		// 				  scales: {
		// 					  y: {
		// 						  beginAtZero: true
		// 					  }
		// 				  }
		// 			  }				
		// 		  });
				  
				  //сортировка таблицы	
				  document.addEventListener('DOMContentLoaded', () => {
				  const getSort = ({ target }) => {
				  const order = (target.dataset.order = -(target.dataset.order || -1));
				  const index = [...target.parentNode.cells].indexOf(target);
				  const collator = new Intl.Collator(['en', 'ru'], { numeric: true });
				  const comparator = (index, order) => (a, b) => order * collator.compare(
					  a.children[index].innerHTML,
					  b.children[index].innerHTML
				  );

				  for(const tBody of target.closest('table').tBodies)
					  tBody.append(...[...tBody.rows].sort(comparator(index, order)));

				  for(const cell of target.parentNode.cells)
					  cell.classList.toggle('sorted', cell === target);
			  };

			  document.querySelectorAll('.table thead').forEach(tableTH => tableTH.addEventListener('click', () => getSort(event)));

		  });
			  
                
            }
        });
    });
});