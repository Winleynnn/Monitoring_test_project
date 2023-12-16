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

function get_user_stations(){
    get_stations()
    $.ajax({
        url: '',
        type: 'get',
        data: {action: 'get_user_stations', username: $('#user_select option:selected').val()},
        success: function(response){
            var stations = response['stations']
            var rights = response['rights']
            $('.second').empty()
            for (stat in stations){
            let column = document.createElement('div')
            column.classList.add('info')
            let up = document.createElement('div')
            up.classList.add('up')
            let stat_name = document.createElement('h3')
            let check_box = document.createElement('label')
            let download_box = document.createElement('label')
            let check_input = document.createElement('input')
            let download_input = document.createElement('input')
            let delete_button = document.createElement('button')
            delete_button.innerHTML = '-'
            delete_button.classList.add('delete_btn')
            delete_button.onclick = function(){delete_station(this.parentNode.parentNode);};
            stat_name.innerHTML = stations[stat]
            check_input.type = 'checkbox'
            download_input.type = 'checkbox'
            check_input.value = 'check'
            download_input.value = 'download'
            check_input.name = stations[stat]
            download_input.name = stations[stat]
            for (right in rights[stat])
            {
            if (rights[stat].includes(check_input.value))
                check_input.checked = true
            if (rights[stat].includes(download_input.value))
                download_input.checked = true
            }
            check_box.innerHTML = 'check'
            download_box.innerHTML = 'download'
            check_box.appendChild(check_input)
            download_box.appendChild(download_input)
            up.appendChild(stat_name)
            up.appendChild(delete_button)
            column.appendChild(up)
            column.appendChild(check_box)
            column.appendChild(download_box)
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
    let check_box = document.createElement('label')
    let download_box = document.createElement('label')
    let check_input = document.createElement('input')
    let download_input = document.createElement('input')
    let temp = $('#station_add option:selected').val()
    stat_name.innerHTML = temp
    $('#station_add option:selected').remove()
    check_input.type = 'checkbox'
    download_input.type = 'checkbox'
    check_input.value = 'check'
    download_input.value = 'download'
    check_box.innerHTML = 'check'
    download_box.innerHTML = 'download'
    check_input.name = temp
    download_input.name = temp
    check_box.appendChild(check_input)
    download_box.appendChild(download_input)
    let up = document.createElement('div')
    let delete_button = document.createElement('button')
    delete_button.innerHTML = '-'
    delete_button.onclick = function(){delete_station(this.parentNode.parentNode);};
    delete_button.classList.add('delete_btn')
    up.classList.add('up')
    up.appendChild(stat_name)
    up.appendChild(delete_button)
    column.appendChild(up)
    column.appendChild(check_box)
    column.appendChild(download_box)
    $('.second').append(column)
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
    console.log(csrftoken)
    var info = {}
    $(".info").each(function(){
        // console.log(this.firstChild.firstChild.innerHTML)
        var temp = []
        
        console.log($(this).children('label').children('input:checked').length)
        if ($(this).children('label').children('input:checked').length != 0)
        {
            $(this).children('label').children('input:checked').each(function(){
            temp.push(this.value)
        })
        info[this.firstChild.firstChild.innerHTML] = temp
        }
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
    console.log(info)
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
    // const BASE_URL = window.location.href;
    // const API_URL = BASE_URL + '/add';
    // const request = new Request(
    //     API_URL,
    //     {headers: {'X-CSRFToken': csrftoken}}
    // );
    // fetch(request, {
    //     method: 'POST',
    //     mode: 'same-origin',
    //     data: {stations: info}  // Do not send CSRF token to another domain.
    // }).then(function(response) {
    //     console.log(info)
    // });
    })
}