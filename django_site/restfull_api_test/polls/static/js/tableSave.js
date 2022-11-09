// Quick and simple export target #table_id into a csv
function download_table_as_csv(table_id, separator = ';') {
    // Select rows from table_id
    var rows = document.querySelectorAll('table#' + table_id + ' tr');
    // Construct csv
    var csv = [];
    for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll('td, th');
        for (var j = 0; j < cols.length; j++) {
            // Clean innertext to remove multiple spaces and jumpline (break csv)
            var data = cols[j].innerText.replace(/(\r\n|\n|\r)/gm, '').replace(/(\s\s)/gm, ' ')
            // Escape double-quote with double-double-quote (see https://stackoverflow.com/questions/17808511/properly-escape-a-double-quote-in-csv)
            data = data.replace(/"/g, '""')
            // Push escaped string
            row.push(data)
        }
        csv.push(row.join(separator))
    }
    var csv_string = csv.join('\n');
    // Download it
    info_array = get_info()
    station = info_array[0]
    firstDate = info_array[1]
    secondDate = info_array[2]
    mode = info_array[3]
    var filename = `${station}_${mode}_${firstDate}_${secondDate}.csv`;
    var link = document.createElement('a');
    link.style.display = 'none';
    link.setAttribute('target', '_blank');
    link.setAttribute('href', 'data:text/csv;charset=cp1251,' + encodeURIComponent(csv_string));
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function download_table_as_xlsx(table_id) {
    /* Create worksheet from HTML DOM TABLE */
    var wb = XLSX.utils.table_to_book(document.getElementById(table_id));
    /* Export to file (start a download) */
    info_array = get_info()
    station = info_array[0]
    firstDate = info_array[1]
    secondDate = info_array[2]
    mode = info_array[3]
    XLSX.writeFile(wb, `${station}_${mode}_${firstDate}_${secondDate}.xlsx`);
  };

function get_info() {
    station = $('#select_station option:selected').text()
    firstDate = $('#first_date').val()
    secondDate = $('#second_date').val()
    mode = $('#select_mode option:selected').val()
    return([station, firstDate, secondDate, mode])
}