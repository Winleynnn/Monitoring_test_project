$(document).ready(function(){
    $.ajax({
        url: '',
        type: 'get',
        data: '',
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
            stations = response['stations']
            var sel = $('#station_add')
            for (station in stations)
            {
                let opt = document.createElement('option')
                opt.value = stations[station]
                opt.text = stations[station]
                sel.append(opt, null)
                // $('#user_select').innerHTML += "<option value='" + username + "'>" + username + "</option>"
            }
    }
})
})