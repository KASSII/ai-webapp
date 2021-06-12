$.format = function(format){
    var i = 0,
        j = 0,
        r = "",
        next = function(args){
            j += 1; i += 1;
            return args[j] !== void 0 ? args[j] : "";
        };

    for(i=0; i<format.length; i++){
        if(format.charCodeAt(i) === 37){
            switch(format.charCodeAt(i+1)){
                case 115: r += next(arguments); break;
                case 100: r += Number(next(arguments)); break;
                default: r += format[i]; break;
            }
        } else {
            r += format[i];
        }
    }
    return r;
};

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}