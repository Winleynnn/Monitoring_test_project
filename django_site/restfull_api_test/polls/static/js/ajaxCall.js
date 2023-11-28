// function createChart1(label, dataset, dataset2){
    // if (label[0] == null) 
    // {
    //     $('#messageNoInfo1').text('Данных за выбранный период не найдено')
    //     $('#messageNoInfo2').text('Данных за выбранный период не найдено')
    //     $('#myChart').hide()
    //     $('#myChart2').hide()
    //     $('#myTable').hide()
    // }
    // else
    // {
    //     $('#messageNoInfo1').text('')
    //     $('#messageNoInfo2').text('')
    //     $('#myChart').show()
    //     $('#myChart2').show()
    //     $('#myTable').show()
    //     var ctx = document.getElementById('myChart').getContext('2d');
    //     myChart.destroy()
    //     myChart = new Chart(ctx, {
    //         type: 'line',
    //         data: {														
    //             labels: label,
    //             datasets: dataset,
    //             },
    //         options: {
    //             scales: {
    //                 y: {
    //                     beginAtZero: true
    //                 }
    //             }
    //         }				
    //     });
    //     var ctx2 = document.getElementById('myChart2').getContext('2d');
    //     myChart2.destroy()
    //     myChart2 = new Chart(ctx2, {
    //         type: 'line',
    //         data: {														
    //             labels: label,
    //             datasets: dataset2,
    //             },
    //         options: {
    //             scales: {
    //                 y: {
    //                     beginAtZero: true
    //                 }
    //             }
    //         }				
    //     })
    // }
// };

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

var today = new Date();
var dd = today.getDate();
var mm = today.getMonth()+1;
var yyyy = today.getFullYear();

if(dd<10) {
    dd = '0'+dd
} 

if(mm<10) {
    mm = '0'+mm
} 

today = yyyy + '-' + mm + '-' + dd;
$('#second_date').attr({
    'max' : today
})

// $(".custom-select-trigger").on('DOMSubtreeModified', function()
// {
//     timeData = 
//         {
//         first_date: first_date,
//         second_date: second_date,
//         selected_station: $('#select_station option:selected').text(),
//         selected_mode: $('#select_mode option:selected').val(),
//         // action: 'take_info'
//         }        
//     ajaxCall(timeData)
// })
$("#button_date").on('click', function()
{
    timeData = 
        {
        first_date: $('#first_date').val(),
        second_date: $('#second_date').val(),
        selected_station: $('#select_station option:selected').text(),
        selected_mode: $('#select_mode option:selected').val(),
        // action: 'take_info'
        }
    first_date = $('#first_date').val()
    second_date = $('#second_date').val()        
    ajaxCall(timeData)
})
    // get_stations()
    get_info()
});

function dropdown()
{
 
}

function get_stations(){
    $.ajax({
        url: '',
        type: 'get',
        data: {action: 'get_stations'},
        success: function(response){
            var stations = response['stations']
            console.log(stations[0])
            $('#select_station').empty()
            for (var i = 0; i < stations.length; i++)
                $('#select_station').append("<option value='" + stations[i] + "'>" + stations[i] +"</option>")

            }
    })
}

function get_info(){
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
    
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1;
    var yyyy = today.getFullYear();

    if(dd<10) {
        dd = '0'+dd
    } 

    if(mm<10) {
        mm = '0'+mm
    } 

    today = yyyy + '-' + mm + '-' + dd;
    $('#second_date').attr({
        'max' : today
    })

    $(".custom-select-trigger").on('DOMSubtreeModified', function()
    {
        timeData = 
            {
            first_date: first_date,
            second_date: second_date,
            selected_station: $('#select_station option:selected').text(),
            selected_mode: $('#select_mode option:selected').val(),
            // action: 'take_info'
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
            selected_mode: $('#select_mode option:selected').val(),
            // action: 'take_info'
            }
        first_date = $('#first_date').val()
        second_date = $('#second_date').val()        
        ajaxCall(timeData)
    })
}

function ajaxCall(timeData){
    $.ajax({
        url: '',
        type: 'get',
        data: timeData,
        success: function(response){
            var columns = response['names']
            var aliases = response['aliases']
            // var dates = response['date']
            // var variables = []
            // for (column in columns)
            //     variables.append(response[columns[column]])
            // var air_temp = response['air_temp_avg']
            // var soil_temp = response['soil_temp_avg']
            // var humidity = response['relative_humidity_avg']
            // var soil_moisture = response['soil_moisture']
            var chart = response['graph']
            var stat = response['statistics']
            var info = response['information']
            var corr_chart = response['correlation_chart']
            var box_chart = response['box_plot_chart']
            var graphic = $('.graphic')[0]
            var graphic2 = $('.graphic2')[0]
            var graphic3 = $('.graphic3')[0]
            // id = graphic.childNodes[0].childNodes[2].id

            // graphic.childNodes[0].childNodes[2].id = id
            graphic.innerHTML = chart
            graphic2.innerHTML = corr_chart
            graphic3.innerHTML = box_chart

            var statistics = $('.stat')[0]
            var information = $('.info')[0]
            statistics.innerHTML = stat
            information.innerHTML = info
            // console.log(stat)
            // console.log(info)
            var arr = graphic.getElementsByTagName('script')
            for (var n = 0; n < arr.length; n++)
                eval(arr[n].innerHTML)
            var arr = graphic2.getElementsByTagName('script')
            for (var n = 0; n < arr.length; n++)
                eval(arr[n].innerHTML)
            var arr = graphic3.getElementsByTagName('script')
            for (var n = 0; n < arr.length; n++)
                eval(arr[n].innerHTML)

            tableParent = document.getElementById('myTable').parentNode
            $("#myTable").remove()
            tableChild = document.createElement('table')
            tableChild.id = 'myTable'
            tableChild.classList.add('table')
            var newRow = tableChild.insertRow(0);
            for (var n = 0; n < aliases.length; n++)
                newRow.insertCell(n).outerHTML = '<th>' + aliases[n] + '</th>'
            // newRow.insertCell(0).outerHTML = '<th>Дата</th>';
            // newRow.insertCell(1).outerHTML = '<th>Средняя температура воздуха, °C</th>';
            // newRow.insertCell(2).outerHTML = '<th>Средняя температура почвы, °C</th>';
            // newRow.insertCell(3).outerHTML = '<th>Относительная влажность воздуха, %</th>';
            // newRow.insertCell(4).outerHTML = '<th>Влажность почвы, %</th>';
            tableChild.appendChild(newRow);
            console.log(columns)
            console.log(response[columns[0]].length)
            console.log(response[columns[0]])
            for (var n in response[columns[0]])
            {
                var newRow = tableChild.insertRow(n.indexOf);
                for (var i = 0; i < columns.length; i++)
                    newRow.insertCell(i).innerHTML = response[columns[i]][n]
                tableChild.appendChild(newRow)
            }
            // for (var i in dates)
            // {
            //     var newRow = tableChild.insertRow(i.indexOf);
            //     newRow.insertCell(0).innerHTML = dates[i];
            //     newRow.insertCell(1).innerHTML = air_temp[i];
            //     newRow.insertCell(2).innerHTML = soil_temp[i];
            //     newRow.insertCell(3).innerHTML = humidity[i];
            //     newRow.insertCell(4).innerHTML = soil_moisture[i];            
            //     tableChild.appendChild(newRow);           
            // }

            tableParent.appendChild(tableChild)

            $("#myTable tbody").remove()
            $('#myTable tr:has(td)').wrapAll('<tbody></tbody>')
            $("#myTable tbody").prependTo("#myTable")
            $('#myTable tr:has(th)').wrapAll('<thead></thead>')
            $("#myTable thead").prependTo("#myTable")
            // if (response.name == "Station_0020CF3B")
            // {
            //     var dates = response['date']
            //     var air_temp = response['air_temp_avg']
            //     var soil_temp = response['soil_temp_avg']
            //     var humidity = response['relative_humidity_avg']
            //     var soil_moisture = response['soil_moisture']
            //     var chart = response['graph']
            //     var stat = response['statistics']
            //     var info = response['information']
            //     var corr_chart = response['correlation_chart']
            //     var box_chart = response['box_plot_chart']
            //     var graphic = $('.graphic')[0]
            //     var graphic2 = $('.graphic2')[0]
            //     var graphic3 = $('.graphic3')[0]
            //     // id = graphic.childNodes[0].childNodes[2].id

            //     // graphic.childNodes[0].childNodes[2].id = id
            //     graphic.innerHTML = chart
            //     graphic2.innerHTML = corr_chart
            //     graphic3.innerHTML = box_chart

            //     var statistics = $('.stat')[0]
            //     var information = $('.info')[0]
            //     statistics.innerHTML = stat
            //     information.innerHTML = info
            //     console.log(stat)
            //     console.log(info)
            //     var arr = graphic.getElementsByTagName('script')
            //     for (var n = 0; n < arr.length; n++)
            //         eval(arr[n].innerHTML)

            //     var arr = graphic2.getElementsByTagName('script')
            //     for (var n = 0; n < arr.length; n++)
            //         eval(arr[n].innerHTML)

            //     var arr = graphic3.getElementsByTagName('script')
            //     for (var n = 0; n < arr.length; n++)
            //         eval(arr[n].innerHTML)


            //     tableParent = document.getElementById('myTable').parentNode
            //     $("#myTable").remove()
            //     tableChild = document.createElement('table')
            //     tableChild.id = 'myTable'
            //     tableChild.classList.add('table')
            //     var newRow = tableChild.insertRow(0);
            //     newRow.insertCell(0).outerHTML = '<th>Дата</th>';
            //     newRow.insertCell(1).outerHTML = '<th>Средняя температура воздуха, °C</th>';
            //     newRow.insertCell(2).outerHTML = '<th>Средняя температура почвы, °C</th>';
            //     newRow.insertCell(3).outerHTML = '<th>Относительная влажность воздуха, %</th>';
            //     newRow.insertCell(4).outerHTML = '<th>Влажность почвы, %</th>';
                

            //     tableChild.appendChild(newRow);
            //     for (var i in dates)
            //     {
            //         var newRow = tableChild.insertRow(i.indexOf);
            //         newRow.insertCell(0).innerHTML = dates[i];
            //         newRow.insertCell(1).innerHTML = air_temp[i];
            //         newRow.insertCell(2).innerHTML = soil_temp[i];
            //         newRow.insertCell(3).innerHTML = humidity[i];
            //         newRow.insertCell(4).innerHTML = soil_moisture[i];            
            //         tableChild.appendChild(newRow);           
            //     }

            //     tableParent.appendChild(tableChild)

            //     $("#myTable tbody").remove()
            //     $('#myTable tr:has(td)').wrapAll('<tbody></tbody>')
            //     $("#myTable tbody").prependTo("#myTable")
            //     $('#myTable tr:has(th)').wrapAll('<thead></thead>')
            //     $("#myTable thead").prependTo("#myTable")
                
            //     // var S_0020CF3B_dataset_temp = 
            //     // [
            //     //     {                     
            //     //         label: 'Средняя температура воздуха, °C',
            //     //         data: air_temp,
            //     //         backgroundColor: ['rgba(255, 255,255, 0.2)'],
            //     //         borderColor: ['rgba(200, 0, 15, 1)'],
            //     //         borderWidth: 2
            //     //     },
            //     //     {
            //     //         label: 'Средняя температура почвы, °C',
            //     //         data: soil_temp,
            //     //         backgroundColor: ['rgba(255, 255, 255, 0.2)'],
            //     //         borderColor: ['rgba(9, 132, 0, 1)'],                            
            //     //         borderWidth: 2
            //     //     }
            //     // ]

            //     // var S_0020CF3B_dataset_water = 
            //     // [
            //     //     {                     
            //     //         label: 'Относительная влажность воздуха, %',
            //     //         data: humidity,
            //     //         backgroundColor: ['rgba(255, 255,255, 0.2)'],
            //     //         borderColor: ['rgba(200, 0, 15, 1)'],
            //     //         borderWidth: 2
            //     //     },
            //     //     {
            //     //         label: 'Средняя влажность почвы, %',
            //     //         data: soil_moisture,
            //     //         backgroundColor: ['rgba(255, 255, 255, 0.2)'],
            //     //         borderColor: ['rgba(9, 132, 0, 1)'],                            
            //     //         borderWidth: 2
            //     //     }
            //     // ]
            //     // createChart1(dates, S_0020CF3B_dataset_temp, S_0020CF3B_dataset_water);
            // }

            // if (response.name == "Station_002099C5")
            // {
            //     var dates = response['dates']
            //     var air_temp = response['air_temp_avg']
            //     var humidity = response['relative_humidity_avg']
            //     var soil_temp_1 = response['soil_temp_1']
            //     var soil_temp_2 = response['soil_temp_2']
            //     var soil_temp_3 = response['soil_temp_3']
            //     var predict = response['predict']

            //     var chart = response['graph']
            //     var graphic = $('.graphic')[0]
            //     graphic.innerHTML = chart
            //     var arr = graphic.getElementsByTagName('script')
            //     for (var n = 0; n < arr.length; n++)
            //         eval(arr[n].innerHTML)


            //     tableParent = document.getElementById('myTable').parentNode
            //     $("#myTable").remove()
            //     tableChild = document.createElement('table')
            //     tableChild.id = 'myTable'
            //     tableChild.classList.add('table')
            //     var newRow = tableChild.insertRow(0);
            //     newRow.insertCell(0).outerHTML = '<th>Дата</th>';
            //     newRow.insertCell(1).outerHTML = '<th>Средняя температура воздуха, °C</th>';
            //     newRow.insertCell(2).outerHTML = '<th>Относительная влажность воздуха, %</th>';
            //     newRow.insertCell(3).outerHTML = '<th>Средняя температура почвы, °C</th>';
            //     newRow.insertCell(4).outerHTML = '<th>Средняя температура почвы, °C</th>';
            //     newRow.insertCell(5).outerHTML = '<th>Средняя температура почвы, °C</th>';
            //     newRow.insertCell(6).outerHTML = '<th>Прогнозируемая влажность почвы, %</th>';
            //     tableChild.appendChild(newRow);
            //     for (var i in dates)
            //     {
            //         var newRow = tableChild.insertRow(i.indexOf);
            //         newRow.insertCell(0).innerHTML = dates[i];
            //         newRow.insertCell(1).innerHTML = air_temp[i];
            //         newRow.insertCell(2).innerHTML = humidity[i];
            //         newRow.insertCell(3).innerHTML = soil_temp_1[i];
            //         newRow.insertCell(4).innerHTML = soil_temp_2[i];    
            //         newRow.insertCell(5).innerHTML = soil_temp_3[i];    
            //         newRow.insertCell(6).innerHTML = predict[i];            
            //         tableChild.appendChild(newRow);           
            //     }

            //     tableParent.appendChild(tableChild)
                
            //     $("#myTable tbody").remove()
            //     $('#myTable tr:has(td)').wrapAll('<tbody></tbody>')
            //     $("#myTable tbody").prependTo("#myTable")
            //     $('#myTable tr:has(th)').wrapAll('<thead></thead>')
            //     $("#myTable thead").prependTo("#myTable")
                

            //     // var S_002099C5_dataset = 
            //     // [
            //     //     {                     
            //     //         label: 'Средняя температура воздуха, °C',
            //     //         data: air_temp,
            //     //         backgroundColor: ['rgba(255, 255,255, 0.2)'],
            //     //         borderColor: ['rgba(200, 0, 15, 1)'],
            //     //         borderWidth: 2
            //     //     },
            //     //     {
            //     //         label: 'Относительная влажность воздуха, %',
            //     //         data: humidity,
            //     //         backgroundColor: ['rgba(255, 255, 255, 0.2)'],
            //     //         borderColor: ['rgba(9, 132, 0, 1)'],                            
            //     //         borderWidth: 2
            //     //     },
            //     //     {
            //     //         label: 'Прогнозируемая влажность почвы, %',
            //     //         data: predict,
            //     //         backgroundColor: ['rgba(255, 255, 255, 0.2)'],
            //     //         borderColor: ['rgba(12, 0, 134, 1)'],                            
            //     //         borderWidth: 2
            //     //     }
            //     // ]

            //     // var S_002099C5_dataset_temp = 
            //     // [
            //     //     {                     
            //     //         label: 'Температура почвы 1, °C',
            //     //         data: soil_temp_1,
            //     //         backgroundColor: ['rgba(255, 255,255, 0.2)'],
            //     //         borderColor: ['rgba(200, 0, 15, 1)'],
            //     //         borderWidth: 2
            //     //     },
            //     //     {
            //     //         label: 'Температура почвы 2, °C',
            //     //         data: soil_temp_2,
            //     //         backgroundColor: ['rgba(255, 255, 255, 0.2)'],
            //     //         borderColor: ['rgba(9, 132, 0, 1)'],                            
            //     //         borderWidth: 2
            //     //     },
            //     //     {
            //     //         label: 'Температура почвы 3, °C',
            //     //         data: soil_temp_3,
            //     //         backgroundColor: ['rgba(255, 255, 255, 0.2)'],
            //     //         borderColor: ['rgba(9, 0, 243, 1)'],                            
            //     //         borderWidth: 2
            //     //     }
            //     // ]
            //     // createChart1(dates, S_002099C5_dataset, S_002099C5_dataset_temp);
            // }

            // // 00000235: id, date, air_temp_avg, relative_humidity_avg, dew_point, wind_speed_avg, wind_speed_max

            // if (response.name == 'Station_00000235')
            // {
            //     var dates = response['dates']
            //     var air_temp = response['air_temp_avg']
            //     var humidity = response['relative_humidity_avg']
            //     var dew_point = response['dew_point']
            //     var wind_speed_avg = response['wind_speed_avg']
            //     var wind_speed_max = response['wind_speed_max']

            //     var chart = response['graph']
            //     var graphic = $('.graphic')[0]
            //     graphic.innerHTML = chart
            //     var arr = graphic.getElementsByTagName('script')
            //     for (var n = 0; n < arr.length; n++)
            //         eval(arr[n].innerHTML)

            //     tableParent = document.getElementById('myTable').parentNode
            //     $("#myTable").remove()
            //     tableChild = document.createElement('table')
            //     tableChild.id = 'myTable'
            //     tableChild.classList.add('table')
            //     var newRow = tableChild.insertRow(0);
            //     newRow.insertCell(0).outerHTML = '<th>Дата</th>';
            //     newRow.insertCell(1).outerHTML = '<th>Средняя температура воздуха, °C</th>';
            //     newRow.insertCell(2).outerHTML = '<th>Относительная влажность воздуха, %</th>';
            //     newRow.insertCell(3).outerHTML = '<th>Точка росы, °C</th>';
            //     newRow.insertCell(4).outerHTML = '<th>Средняя скорость ветра, м/с</th>';
            //     newRow.insertCell(5).outerHTML = '<th>Максимальная скорость ветра, м/с</th>';
            //     tableChild.appendChild(newRow);
            //     for (var i in dates)
            //     {
            //         var newRow = tableChild.insertRow(i.indexOf);
            //         newRow.insertCell(0).innerHTML = dates[i];
            //         newRow.insertCell(1).innerHTML = air_temp[i];
            //         newRow.insertCell(2).innerHTML = humidity[i];
            //         newRow.insertCell(3).innerHTML = dew_point[i];
            //         newRow.insertCell(4).innerHTML = wind_speed_avg[i];    
            //         newRow.insertCell(5).innerHTML = wind_speed_max[i];         
            //         tableChild.appendChild(newRow);           
            //     }

            //     tableParent.appendChild(tableChild)
                
            //     $("#myTable tbody").remove()
            //     $('#myTable tr:has(td)').wrapAll('<tbody></tbody>')
            //     $("#myTable tbody").prependTo("#myTable")
            //     $('#myTable tr:has(th)').wrapAll('<thead></thead>')
            //     $("#myTable thead").prependTo("#myTable")
                

                // var S_002099C5_dataset = 
                // [
                //     {                     
                //         label: 'Средняя температура воздуха, °C',
                //         data: air_temp,
                //         backgroundColor: ['rgba(255, 255,255, 0.2)'],
                //         borderColor: ['rgba(200, 0, 15, 1)'],
                //         borderWidth: 2
                //     },
                //     {
                //         label: 'Относительная влажность воздуха, %',
                //         data: humidity,
                //         backgroundColor: ['rgba(255, 255, 255, 0.2)'],
                //         borderColor: ['rgba(9, 132, 0, 1)'],                            
                //         borderWidth: 2
                //     },
                //     {
                //         label: 'Точка росы, °C',
                //         data: dew_point,
                //         backgroundColor: ['rgba(255, 255, 255, 0.2)'],
                //         borderColor: ['rgba(12, 0, 134, 1)'],                            
                //         borderWidth: 2
                //     }
                // ]

                // var S_002099C5_dataset_temp = 
                // [
                //     {                     
                //         label: 'Средняя скорость ветра, м/с',
                //         data: wind_speed_avg,
                //         backgroundColor: ['rgba(255, 255,255, 0.2)'],
                //         borderColor: ['rgba(200, 0, 15, 1)'],
                //         borderWidth: 2
                //     },
                //     {
                //         label: 'Максимальная скорость ветра, м/с',
                //         data: wind_speed_max,
                //         backgroundColor: ['rgba(255, 255, 255, 0.2)'],
                //         borderColor: ['rgba(9, 132, 0, 1)'],                            
                //         borderWidth: 2
                //     }
                // ]
                // createChart1(dates, S_002099C5_dataset, S_002099C5_dataset_temp);
            }
              
    //           //сортировка таблицы
    //           document.addEventListener('DOMContentLoaded', () => {
    //           const getSort = ({ target }) => {
    //           const order = (target.dataset.order = -(target.dataset.order || -1));
    //           const index = [...target.parentNode.cells].indexOf(target);
    //           const collator = new Intl.Collator(['en', 'ru'], { numeric: true });
    //           const comparator = (index, order) => (a, b) => order * collator.compare(
    //               a.children[index].innerHTML,
    //               b.children[index].innerHTML
    //           );

    //           for(const tBody of target.closest('table').tBodies)
    //               tBody.append(...[...tBody.rows].sort(comparator(index, order)));

    //           for(const cell of target.parentNode.cells)
    //               cell.classList.toggle('sorted', cell === target);
    //       };

    //       document.querySelectorAll('.table thead').forEach(tableTH => tableTH.addEventListener('click', () => getSort(event)));

    //   });	  
            
        // }
    });
}