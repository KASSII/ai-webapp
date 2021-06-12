$('#result-title').hide();

// アップロードボタンを押した時の関数（formのfileとリンクさせる）
function OnLinkClick() {
    $('#upload-file').click();
    return false;
}

// ファイルがアップロードされた時の関数
// 画像をbase64で読み込み、各タスクのinference_ajax関数を呼び出す
$('#upload-file').on('change', function(e) {
    // ローディング画面を表示（非表示は各inference_ajax()内で行う）
    $.blockUI({
        message: 'Now Analyzing',
        css: {
            border: 'none',
            padding: '10px',
            backgroundColor: '#333',
            opacity: .5,
            color: '#fff'
        },
        overlayCSS: {
            backgroundColor: '#000',
            opacity: 0.6
        }
    });

    // result画面を初期化
    $('#result').empty();

    var encode_image = ""
    var file = e.target.files[0];
    var fr = new FileReader();
    fr.onload=function(evt) {
        encode_image = evt.target.result;
        var html = $.format('<img src="%s" />', evt.target.result);
        $("#preview").empty();
        $("#preview").append(html);
        inference_ajax(encode_image);
    }
    fr.readAsDataURL(file)
});