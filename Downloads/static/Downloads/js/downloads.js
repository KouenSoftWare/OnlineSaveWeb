/**
 * Created by kouen on 2017/9/29.
 */

$(".topic").click(e=>{
    let text = e.currentTarget.computedName;
    $("#btn_select_topic")[0].innerHTML = text + ' <span class="caret"></span>'
});

$(`#date_current`).datetimepicker({format: 'YYYY-MM-DD'});

$(".enter").click(e=>{
    let topic = $("#btn_select_topic")[0].innerText;
    let date = $("#date_current")[0].value;
    if (date !== "" && topic !== "Topic选择") {
        $.get(`/table/?topic=${topic}&date=${date}`, (d)=>{
            table.rows('').remove().draw();
            for (let i of d.data)
                table.row.add(i).draw();

        })
    }
});

let table = $('#table_data').DataTable({
    pageLength: 10,
    columns: [
        {"data": "name"},
        {"data": "date"},
        {"data": "size"}
    ],
    "ajax": {
        "url": "/table",
    }
});

table.on('click', 'tr', function () {
    let data = table.row( this ).data();
    if (data !== undefined){
        location.href=`/downFile?path=${data.path}&name=${data.name}`;
    }
} );
