function createChart1(label, dataset, dataset2){
    if (label[0] == null) 
    {
        $('#messageNoInfo1').text('no info sorry')
        $('#messageNoInfo2').text('no info sorry')
        $('#myChart').hide()
        $('#myChart2').hide()
        $('#myTable').hide()

    }
    else
    {
        $('#messageNoInfo1').text('')
        $('#messageNoInfo2').text('')
        $('#myChart').show()
        $('#myChart2').show()
        $('#myTable').show()
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
    }
};

$(document).ready(function(){
    var timeData = 
        {
        first_date: $('#first_date').val(),
        second_date: $('#second_date').val(),
        selected_station: $('#select_station option:selected').text(),
        selected_mode: $('#select_mode option:selected').val()
        }
    var first_date = $('#first_date').val()
    var second_date = $('#second_date').val()
    ajaxCall(timeData)
    $(".custom-select-trigger").on('DOMSubtreeModified', function()
    {
        timeData = 
            {
            first_date: first_date,
            second_date: second_date,
            selected_station: $('#select_station option:selected').text(),
            selected_mode: $('#select_mode option:selected').val()
            }        
        ajaxCall(timeData)
    })
    $("#button_date").on('click', function()
    {
        timeData = 
            {
            first_date: $('#first_date').val(),
            second_date: $('#second_date').val(),
            selected_station: $('#select_station option:selected').text(),
            selected_mode: $('#select_mode option:selected').val()
            }
        first_date = $('#first_date').val()
        second_date = $('#second_date').val()        
        ajaxCall(timeData)
    })
    $("#first_date").on('change', function()
    {
        $("#second_date").attr({
            'min' : $("#first_date").val()
        })
    })
    $("#second_date").on('change', function()
    {
        $("#first_date").attr({
            'max' : $("#second_date").val()
        })
    })
});

function ajaxCall(timeData){
    $.ajax({
        url: '',
        type: 'get',
        data: timeData,
        success: function(response){
            if (response.name == "Station_0020CF3B")
            {
                var dates = response['dates']
                var air_temp = response['air_temp_avg']
                var soil_temp = response['soil_temp_avg']
                var humidity = response['relative_humidity_avg']
                var soil_moisture = response['soil_moisture']
                $('#first_date').attr({
                    'min' : response.min_date
                })
                $('#second_date').attr({
                    'max' : response.max_date
                })
                
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
            }

            if (response.name == "Station_002099C5")
            {                    
                var dates = response['dates']
                var air_temp = response['air_temp_avg']
                var humidity = response['relative_humidity_avg']
                var soil_temp_1 = response['soil_temp_1']
                var soil_temp_2 = response['soil_temp_2']
                var soil_temp_3 = response['soil_temp_3']

                $('#first_date').attr({
                    'min' : response.min_date
                })
                $('#second_date').attr({
                    'max' : response.max_date
                })                    

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
            }
              
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
}