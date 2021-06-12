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
            html += $.format('<img src="data:image/jpeg;base64,%s" width="600" style="margin-bottom: 30px;">', response["overray_image"]);
            html += $.format('<img src="data:image/jpeg;base64,%s" width="600" style="margin-bottom: 30px;">', response["mask"]);
            html += '<table width="70%">';
            html += '<tr><th>Color</th><th>Label</th></tr>';
            $.each(response["label_map"], function(i, val) {
                html += $.format('<tr><td align="center"><canvas id="rectangle%d" width="25" height="25"></canvas></td><td align="center">%s</td></tr>', i, val["name"]);
            });
            $("#result").append(html);

            $.each(response["label_map"], function(i, val) {
                var canvas = document.getElementById('rectangle' + String(i));
                var context = canvas.getContext('2d');
                context.fillStyle = $.format("rgb(%d, %d, %d)", val["color"][0], val["color"][1], val["color"][2]);
                context.fillRect(0,0,25,25);
            });
            $.unblockUI();
        },
        error: function (response) {
            $.unblockUI();
            alert(response["responseJSON"]["error_message"]);
        }
    });
}