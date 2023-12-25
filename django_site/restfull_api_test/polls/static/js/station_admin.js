$(document).ready(function(){
    $.ajax({
        url: '',
        type: 'get',
        data: {action: 'load_info'},
        success: function(response){
            usernames = response['usernames']
            var sel = $('#user_select')
            for (username in usernames)
            {
                let opt = document.createElement('option')
                opt.value = usernames[username]
                opt.text = usernames[username]
                sel.append(opt, null)
                // $('#user_select').innerHTML += "<option value='" + username + "'>" + username + "</option>"
            }            
            get_stations()
            setTimeout(() => {get_user_stations()}, 50);
        }
    })
})

function get_stations(){
    $.ajax({
    url: '',
    type: 'get',
    data: {action: 'load_info'},
    success: function(response){
        stations = response['stations']
        var sel = $('#station_add')
        sel.empty()
        for (station in stations)
        {
            let opt = document.createElement('option')
            opt.value = stations[station]
            opt.text = stations[station]
            sel.append(opt, null)
        }
    }
})
}

var stations, rights

function get_user_stations(){
    get_stations()
    $.ajax({
        url: '',
        type: 'get',
        data: {action: 'get_user_stations', username: $('#user_select option:selected').val()},
        success: function(response){
            stations = response['stations']
            rights = response['rights']
            console.log(stations)
            console.log(rights)
            $('.second').empty()
            for (stat in stations){
            let column = document.createElement('div')
            column.classList.add('info')
            let up = document.createElement('div')
            up.classList.add('up')
            let stat_name = document.createElement('h3')
            let info_box = document.createElement('label')
            let stat_box = document.createElement('label')
            let pred_box = document.createElement('label')
            let info_input = document.createElement('input')
            let stat_input = document.createElement('input')
            let pred_input = document.createElement('input')
            let delete_button = document.createElement('button')
            delete_button.innerHTML = '-'
            delete_button.classList.add('delete_btn')
            delete_button.onclick = function(){delete_station(this.parentNode.parentNode);};
            stat_name.innerHTML = stations[stat]
            info_input.type = 'checkbox'
            stat_input.type = 'checkbox'
            pred_input.type = 'checkbox'
            info_input.value = 'check_info'
            stat_input.value = 'check_stat'
            pred_input.value = 'check_pred'
            info_input.name = stations[stat]
            stat_input.name = stations[stat]
            pred_input.name = stations[stat]
            for (right in rights[stat])
            {
            if (rights[stat].includes(info_input.value))
                info_input.checked = true
            if (rights[stat].includes(stat_input.value))
                stat_input.checked = true
            if (rights[stat].includes(pred_input.value))
                pred_input.checked = true
            }
            info_box.appendChild(info_input)
            stat_box.appendChild(stat_input)
            pred_box.appendChild(pred_input)
            info_box.appendChild(document.createTextNode('Просмотр данных'))
            stat_box.appendChild(document.createTextNode('Просмотр статистики'))
            pred_box.appendChild(document.createTextNode('Просмотр прогноза'))
            up.appendChild(stat_name)
            up.appendChild(delete_button)
            column.appendChild(up)
            column.appendChild(info_box)
            column.appendChild(stat_box)
            column.appendChild(pred_box)
            $('.second').append(column)
        }
        //    <div class = "column">
        //    <h3>station_name</h3>
        //    <label><input type="checkbox" value="check">check</label>
        //    <label><input type="checkbox" value="download">download</label>
        //    </div>
        $('#station_add option').each(function(){
            for (i in stations)
            if ($(this).val() == stations[i])
            $(this).remove() 
        })    
    }
    })
}

function add_station(){
    let column = document.createElement('div')
    column.classList.add('info')
    let stat_name = document.createElement('h3')
    let info_box = document.createElement('label')
    let stat_box = document.createElement('label')
    let pred_box = document.createElement('label')
    let info_input = document.createElement('input')
    let stat_input = document.createElement('input')
    let pred_input = document.createElement('input')
    let temp = $('#station_add option:selected').val()
    if (temp != undefined){
    stat_name.innerHTML = temp
    $('#station_add option:selected').remove()
    info_input.type = 'checkbox'
    stat_input.type = 'checkbox'
    pred_input.type = 'checkbox'
    info_input.value = 'check_info'
    stat_input.value = 'check_stat'
    pred_input.value = 'check_pred'
    info_input.name = temp
    stat_input.name = temp
    info_box.appendChild(info_input)
    stat_box.appendChild(stat_input)
    pred_box.appendChild(pred_input)
    info_box.appendChild(document.createTextNode('Просмотр данных'))
    stat_box.appendChild(document.createTextNode('Просмотр статистики'))
    pred_box.appendChild(document.createTextNode('Просмотр прогноза'))
    let up = document.createElement('div')
    let delete_button = document.createElement('button')
    delete_button.innerHTML = '-'
    delete_button.onclick = function(){delete_station(this.parentNode.parentNode);};
    delete_button.classList.add('delete_btn')
    up.classList.add('up')
    up.appendChild(stat_name)
    up.appendChild(delete_button)
    column.appendChild(up)
    column.appendChild(info_box)
    column.appendChild(stat_box)
    column.appendChild(pred_box)
    $('.second').append(column)
    }
}

function delete_station(elem)
{
    console.log('delete')
    let opt = document.createElement('option')
    opt.value = elem.firstChild.firstChild.innerHTML
    opt.text = elem.firstChild.firstChild.innerHTML
    $('#station_add').append(opt, null)
    elem.remove()
}

function upload(){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    // console.log(csrftoken)
    var info = {}
    $(".info").each(function(){
        // console.log(this.firstChild.firstChild.innerHTML)
        var temp = []
        
        // console.log($(this).children('label').children('input:checked').length)
        // if ($(this).children('label').children('input:checked').length != 0)
        // {
        $(this).children('label').children('input:checked').each(function(){
            temp.push(this.value)
        })
        info[this.firstChild.firstChild.innerHTML] = temp
        
        // for (var i in temp)
        // {
        //     console.log(temp)
        //     if (this.name == this)
        //     {
        //     console.log($(this).attr('name'))
        //     console.log($(this).attr('value'))
        //     }
        // }
    })
    // console.log(info)
    const BASE_URL = window.location.href;
    const API_URL = BASE_URL + '/add';
    const request = new Request(
        API_URL,
        {headers: {'X-CSRFToken': csrftoken}}
    );
    $.ajax({
        url: window.location.href + '/add',
        headers: {'X-CSRFToken': csrftoken},
        type: 'post',
        data: JSON.stringify({'stations': info, 'username': $('#user_select option:selected').val()}),
        success: function(response){
            console.log('bruh')
        }
    })
    var stations_upload = Object.keys(info)
    var rights_upload = Object.values(info)
    for (i in stations_upload)
    {
        for (j in info[stations_upload[i]])
        {
            // console.log(info[stations_upload[i]][j] == 'check')
            // console.log(info[stations_upload[i]][j] == 'download')
            if (info[stations_upload[i]][j] == 'check_info')
            info[stations_upload[i]][j] = 'Просмотр данных'
            if (info[stations_upload[i]][j] == 'check_stat')
            info[stations_upload[i]][j] = 'Просмотр статистики'
            if (info[stations_upload[i]][j] == 'check_pred')
            info[stations_upload[i]][j] = 'Просмотр прогноза'
            
        }
    }
    var text = ""
    for (i in rights)
    {
        for (j in rights[i])
        {
            if (rights[i][j] == "check_info")
            rights[i][j] = 'Просмотр данных'
            if (rights[i][j] == "check_stat")
            rights[i][j] = 'Просмотр статистики'
            if (rights[i][j] == "check_pred")
            rights[i][j] = 'Просмотр прогноза'
        }
    }
    for (i in stations)
    {
        if (info[stations[i]])
        {
            for (j in info[stations[i]])
            {
                for (s in rights[i])
                {
                    if (!rights[i].includes(info[stations[i]][j]))
                    {
                        text += "Добавлено разрешение '" + info[stations[i]][j] + "' на станции '" + stations[i] + "'<br>"
                    }
                    if (!info[stations[i]].includes(rights[i][s]))
                    {
                        text += "Удалено разрешение '" + rights[i][s] + "' на станции '" + stations[i] + "'<br>"
                    }
                }
            }
        }
        else
        {
            text += "Удалена станция '" + stations[i] + "'<br>"
        }
    }
    for (a in stations_upload)
    {
        if (!stations.includes(stations_upload[a]))
        {
            text += "Добавлена станция '" + stations_upload[a] + "'<br>"
            for (b in rights_upload[a])
            {
                text += "Добавлено разрешение '" + rights_upload[a][b] + "' на станции '" + stations_upload[a] + "'<br>" 
            }
        }
    }
    console.log(text)
    if (text == "")
    text = "Никаких изменений не было проведено"
    $('#station_text')[0].innerHTML = text
    open_modal()
}

function close_modal()
{
    $('.modal_window').fadeOut();
    $('.window_blackout').fadeOut();
    get_user_stations()
}
function open_modal()
{
    $('.modal_window').fadeIn()
    $('.window_blackout').fadeIn()
}
