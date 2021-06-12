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
            $('#result-title').show();
            $('#result').empty();
            var html = '';
            html += '<table width="70%">';
            html += '<tr><th>Label</th><th>Prob</th></tr>';
            $.each(response["predict"], function(i, val) {
                html += $.format('<tr><td align="center">%s</td><td align="center">%s %</td></tr>', val["label"], String(val["prob"].toFixed(1)));
            });
            $("#result").append(html);
            $.unblockUI();
        },
        error: function (response) {
            $.unblockUI();
            alert(response["responseJSON"]["error_message"]);
        }
    });
}