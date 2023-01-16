const ws = new WebSocket('ws://127.0.0.1:8000/ws/lot/');

$('#id_bid').keyup(function (event){
    if (event.code === 'Enter'){
        $('.send').trigger('submit');
    }
})

ws.onmessage = function (data){
    const user_message = JSON.parse(data.data);
    const new_bid = $(`<div class="message"><b>${user_message.username}:</b>${user_message.message}</div>`);
    $('.lot-window').append(new_bid);
}

$('#lot-form').on('submit',function(e){
        e.preventDefault();
        console.log('form submitted');
        update_lot();
        });

function update_lot() {
    let url_array = document.URL.split('/')
    let id = url_array.at(-2);

    $.ajax({
        url: document.URL,
        type: "POST",
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            bid: $('#id_bid').val(),
            id: id
        },
        success: function (json) {
            if (json.error) {
                $('#results').html("<div style='color:red' class='alert-box' data-alert>" + json.error + "</div>");
            } else {
                $('#id_bid').val('');
                let message = json.bid;
                const username = $('#username').val();
                ws.send(JSON.stringify({'username': username, 'message': message}));
                $("#bid").text(json.bid);
            }
        },
        error: function (xhr, errmsg) {
            $('#results').html("<h6 data-alert>Oops! We have encountered an error:" + errmsg + "</h6>");
        }
    });
}