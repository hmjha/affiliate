// Function to sync database with corresponding page_ids
function sync_database(obj) {
    var $parent = obj.parents(".media").find("#sync-message");

    $.ajax({
        url: "sync_data/",
        type: "POST",
        data:  { post_id : obj.attr("value") },
        timeout: 3000,

        success: function(json) {
            var div_msg = (json.message === "success") ? "Posts synced with database" : "No new links posted to page",
                btn_msg = (json.message === "success") ? "Synced" : "Sync",
                btn_class = (json.message === "success") ? "success" : "default",
                icon_style = (json.message === "success") ? "style='color:white'" : "",
                $alert_div = $("<div class='alert alert-" + json.message + "'>" + div_msg + "</div>");

            $alert_div.hide().appendTo($parent).show(500).delay(1000)
                .slideUp(500, function() {
                    $(this).remove();
                });

            obj.removeClass("btn-primary").addClass("btn-" + btn_class);
            obj.empty().append("<i class='fa fa-refresh'" + icon_style + "></i>&nbsp;&nbsp;&nbsp;" + btn_msg);
        },

        error: function(jqXhr) {
            obj.removeClass("btn-primary").addClass("btn-danger");
            obj.empty().append("<i class='fa fa-refresh' style='color:white'></i>&nbsp;&nbsp;&nbsp;Resync");
            console.log(jqXhr.status + ": " + jqXhr.responseText);
        }
    });
}


// This function gets cookie with a given name
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


// The functions below will create a header with csrftoken
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;

    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
}



$(document).ready(function(){
    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Function to toggle active class
    $(".nav li").each(function(){
        var href = $(this).find('a').attr('href');
        if (href === window.location.pathname) {
            $(this).addClass('active');
        }
    });

    // Function to copy post links
    $('html').on('click', '#copy', function() {
        var $well = $(this).parent().parent().find('#toggle'),
            $button = $(this);

        $well.slideToggle(50, function() {
            $well.is(':visible') ? $button.empty().append('<i class="fa fa-align-left fa-minus-circle"></i> &nbsp;&nbsp;Close') : $button.empty().append('<i class="fa fa-align-left fa-clipboard"></i> &nbsp;&nbsp;Copy Link');
            var element = $well.children('#copy-link').get(0);

            if (document.body.createTextRange) { // ie
                var range = document.body.createTextRange();
                range.moveToElementText(element);
                range.select();
            } else if (window.getSelection) { // moz, opera, webkit
                var selection = window.getSelection();
                var textRange = document.createRange();
                textRange.selectNodeContents(element);
                selection.removeAllRanges();
                selection.addRange(textRange);
            }
        });
    });

    // Function to sync data
    $("#account-data").on('click', "#sync-button", function(event) {
        event.preventDefault();
        var $this = $(this);
        $this.removeClass("btn-default").removeClass("btn-success").removeClass("btn-danger").addClass("btn-primary");
        $this.empty().append("<i class='fa fa-refresh fa-spin' style='color:white'></i>&nbsp;&nbsp;Syncing");
        sync_database($this);
    });
});

