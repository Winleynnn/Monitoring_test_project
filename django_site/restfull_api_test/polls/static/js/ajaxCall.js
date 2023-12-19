$(document).ready(function(){
    var timeData;
    var graphic = $('.graphic')[0]
    var graphic2 = $('.graphic2')[0]
    var graphic3 = $('.graphic3')[0]
    
    $('a[href=#tab1]').click(function(){
        console.log('tab1')
        window.dispatchEvent(new Event('resize'));
    })
    $('a[href=#tab3]').click(function(){
        console.log('tab3')
        window.dispatchEvent(new Event('resize'));
    })
    console.log('ready')
    $.ajax({
        url: '',
        type: 'get',
        data: {action: 'get_station_dates', station: $('#select_station option:selected').text()},
        success: function(response){
            console.log('go ajax')
            console.log(response['max_time'])
            console.log(response['min_time'])
            $('#first_date').attr('max', response['max_time'])
            $('#second_date').attr('max', response['max_time'])
            $('#first_date').attr('min', response['min_time'])
            $('#second_date').attr('min', response['min_time'])
            $('#second_date').val($('#second_date').attr('max'))
            $('#first_date').val((moment($('#second_date').attr('max')).subtract(7, 'days').format('YYYY-MM-DD')))    
            timeData = 
            {
            first_date: $('#first_date').val(),
            second_date: $('#second_date').val(),
            selected_station: $('#select_station option:selected').text(),
            selected_mode: $('#select_mode option:selected').val()
            }
            console.log('ready2')
            console.log(timeData)
        }
    })
    timeData = 
    {
    first_date: $('#first_date').val(),
    second_date: $('#second_date').val(),
    selected_station: $('#select_station option:selected').text(),
    selected_mode: $('#select_mode option:selected').val()
    }
    console.log($('#select_station').children('select').first().text())
    
    get_stations()

    $("#button_date").on('click', function()
    {   
        timeData = 
        {
        first_date: $('#first_date').val(),
        second_date: $('#second_date').val(),
        selected_station: $('#select_station option:selected').text(),
        selected_mode: $('#select_mode option:selected').val(),
        action: 'take_info'
        }
        console.log('button_date')
        console.log(timeData['first_date'])
        console.log(timeData['second_date'])
        ajaxCall(timeData)
    })    
});

function get_info(){
    timeData = 
        {
        first_date: $('#first_date').val(),
        second_date: $('#second_date').val(),
        selected_station: $('#select_station option:selected').text(),
        selected_mode: $('#select_mode option:selected').val()
        }
        console.log('get info')
        ajaxCall(timeData)
}

function get_stations(){
    $.ajax({
        url: '',
        type: 'get',
        data: {action: 'get_stations'},
        success: function(response){
            var stations = response['stations']
            $('#select_station').empty()
            for (var i = 0; i < stations.length; i++)
                $('#select_station').append("<option value='" + stations[i] + "'>" + stations[i] +"</option>")
            $('#select_station').value = $('#select_station')[0].value
            $('.custom-select-trigger').first().text($('#select_station')[0].value)
        $(".custom-select").each(function() {
            var classes = $(this).attr("class"),
                id = $(this).attr("id"),
                name = $(this).attr("name");
            var template = '<div class="' + classes + '">';
            template +=
                '<span class="custom-select-trigger">' +
                $(this).attr("placeholder") +
                "</span>";
            template += '<div class="custom-options">';
            $(this)
                .find("option")
                .each(function() {
                template +=
                    '<span class="custom-option ' +
                    $(this).attr("class") +
                    '" data-value="' +
                    $(this).attr("value") +
                    '">' +
                    $(this).html() +
                    "</span>";
                });
            template += "</div></div>";

            $(this).wrap('<div class="custom-select-wrapper"></div>');
            $(this).hide();
            $(this).after(template);
            });
            $(".custom-option:first-of-type").hover(
            function() {
                $(this)
                .parents(".custom-options")
                .addClass("option-hover");
            },
            function() {
                $(this)
                .parents(".custom-options")
                .removeClass("option-hover");   
            }
            );
            $('.custom-select-trigger')[0].innerHTML = $('#select_station')[0].value
            $(".custom-select-trigger").on("click", function() {
            $("html").one("click", function() {
                $(".custom-select").removeClass("opened");
            });
            $(this)
                .parents(".custom-select")
                .toggleClass("opened");
            event.stopPropagation();
            });
            $(".custom-option").on("click", function() {
            $(this)
                .parents(".custom-select-wrapper")
                .find("select")
                .val($(this).data("value"));
            $(this)
                .parents(".custom-options")
                .find(".custom-option")
                .removeClass("selection");
            $(this).addClass("selection");
            $(this)
                .parents(".custom-select")
                .removeClass("opened");
            $(this)
                .parents(".custom-select")
                .find(".custom-select-trigger")
                .text($(this).text());
            });
            var target = document.querySelector('.custom-select-trigger')
            const observer = new MutationObserver(function(mutations){
                get_time()
                $('.map_element').hide();
            })
            var config = { attributes: true, childList: true, characterData: true };
            observer.observe(target, config)

            var element = document.getElementById('map_element');
            element.style = 'height:800px';
            var map = L.map(element, {zoomControl: false});
            L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            var names = response['names']
            var lats = response['lats']
            var longs = response['longs']
            var target;
            console.log(names)
            console.log(lats)
            console.log(longs)
            for (i in names)
            {
                target = L.latLng(lats[i], longs[i])
                L.marker(target, {icon: L.divIcon({
                    iconSize: "auto",
                    iconAnchor: [30, 60],
                    html: "<div onclick='map_icon()' class = 'map_icon' style='display:flex; flex-direction:column; align-items:center;'><div style='background-color:white; border: 1px solid black;'>" + names[i] + "</div><img style='width:30px; height:50px;' src='https://i.imgur.com/9vgFD7l.png'></div>"
                  })}).addTo(map);
            }

            // Set map's center to target with zoom 14.
            map.setView(target, 3);
            console.log($('#select_station').children('select').first())
        }
    })
}
    
function open_map(){
    $('.map_element').toggle();
}

function map_icon(){
    $('#select_station').val($(event.target).parent().text())
    $('.custom-select-trigger').first().text($(event.target).parent().text())
    $('.map_element').toggle()
    console.log('tap')
    get_time()
}

function get_time(){
    $.ajax({
        url: '',
        type: 'get',
        async:'false',
        data: {action: 'get_station_dates', station: $(".custom-select-trigger").first().text()},
        success: function(response){
            console.log(response['max_time'])
            console.log(response['min_time'])
            $('#first_date').attr('max', response['max_time'])
            $('#second_date').attr('max', response['max_time'])
            $('#first_date').attr('min', response['min_time'])
            $('#second_date').attr('min', response['min_time'])
            $('#second_date').val($('#second_date').attr('max'))
            $('#first_date').val((moment($('#second_date').attr('max')).subtract(7, 'days').format('YYYY-MM-DD')))
        },
        complete: function(response){
            $('#button_date').click()
        }})
}

function ajaxCall(timeData){
    console.log(timeData['action'])
    $.ajax({
        url: '',
        type: 'get',
        data: timeData,
        success: function(response){
            var stations = response['stations']
            var rights = response['rights']
            var columns = response['names']
            var aliases = response['aliases']
            // console.log(response)
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
            console.log(rights[stations.indexOf($('.custom-select-trigger').first().text())])
            console.log(rights)
            console.log(rights[stations.indexOf($('.custom-select-trigger').first().text())].includes("download"))
            if (rights[stations.indexOf($('.custom-select-trigger').first().text())].includes("download"))
            {
                $('#save_buttons:not(:has("#save_csv"))').append('<a href="#" id="save_csv" style="margin-right: 5px;"onclick="download_table_as_csv("myTable");">Download as CSV</a>')
                $('#save_buttons:not(:has("#save_xlsx"))').append('<a href="#" id="save_xlsx" onclick="download_table_as_xlsx("myTable");">Download as XLSX</a>')
            }
            else $('#save_buttons:has(a)').empty()
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