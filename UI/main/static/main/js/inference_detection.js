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
            html += $.format('<img src="data:image/jpeg;base64,%s" width="600" style="margin-bottom: 30px;">', response["draw_image"]);
            html += '<table width="70%">';
            html += '<tr><th></th><th>Label</th><th>Prob</th></tr>';
            $.each(response["predict"], function(i, val) {
                if(val["width"] > val["height"]){
                    html += $.format('<tr><td align="center"><img src="data:image/jpeg;base64,%s" width="100"></td><td align="center">%s</td><td align="center">%s %</td></tr>', val["trim_img"], val["label"], String(val["score"].toFixed(1)));
                }
                else{
                    html += $.format('<tr><td align="center"><img src="data:image/jpeg;base64,%s" height="100"></td><td align="center">%s</td><td align="center">%s %</td></tr>', val["trim_img"], val["label"], String(val["score"].toFixed(1)));
                }
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