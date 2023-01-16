$('#lot-create-btn').click(function (){
    const data_array = $("#lot-create-form").serializeArray();
    let data = {};

    for(let i=0; i<data_array.length; i++){
        data[data_array[i].name] = data_array[i].value;
    }

    $.post('/lot/create/', data, function (data) {
        console.log(data);
        if (data.redirect_url) {
            window.location = data.redirect_url;
        } else {
            $('#lot-create-form').html(data);
        }
    });
});


$('.btn-outline-danger').click(function (){
    let id = $(this).attr("value");
    let url = '/lot/close/'+id+'/';
    data = {closed:true, id:id, csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),}
    $.post(url, data, function (data) {
        if (data.success) {
            location.reload();
        } else {
            $('#lot-create-form').html(data);
        }
    });
})
