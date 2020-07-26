function inference_ajax(encode_image){
    $.ajax({
        type: 'POST',
        url: './',
        dataType: 'json',
        'data': {
            'encode_image': encode_image,
            'csrfmiddlewaretoken': getCookie('csrftoken'),
        },
        success: function (response) {
            var html = $.format('<img src="data:image/jpeg;base64,%s" />', response["overray_image"]);
            $("#preview").empty();
            $("#preview").append(html);

            $('#result').empty();
            var html = $.format('<img src="data:image/jpeg;base64,%s" />', response["mask"]);
            $("#result").append(html);
            $.unblockUI();
        },
        error: function (response) {
            $.unblockUI();
            alert(response["responseJSON"]["error_message"]);
        }
    });
}