// Function to iterate over data and generate html
function createHTML(data, $div) {
    $div.children().remove();

    for (var i=0; i<data.length; i++) {
        var n_view = ((data[i].hasOwnProperty("post_view")) && ($.isNumeric(data[i].post_view))) ? "&nbsp;&nbsp;&nbsp;&nbsp;<i class='fa fa-eye'></i> &nbsp;&nbsp;" + data[i].post_view : "",
            button = (data[i].page == "common") ? "<button class='pull-right btn btn-xs btn-default' id='copy'><i class='fa fa-align-left fa-copy'></i> &nbsp;&nbsp;Copy Link</button></p><div class='well well-sm' id='toggle' style='display: none'><p>Press Ctrl+C to copy</p><p id='copy-link'>" + data[i].post_url + "</p></div></div></div></div>" : "<a class='pull-right btn btn-xs btn-primary'><i class='fa fa-align-left fa-line-chart' style='color: white'></i> &nbsp;&nbsp;Insights</a></p></div></div></div>";

        if (i%3 == 0) {
            var $child_div = $("<div class='row'></div>");
            $div.append($child_div);
        }

        var $info_div = $(
            "<div class='col-sm-4 col-xs-6'><div class='panel panel-default'><div class='panel-thumbnail'><img src='" + data[i].img_url +
            "' class='img-responsive' /></div><div class='panel-body'><p class='lead'><a href=" + data[i].post_url + "target='_blank'>" +
            data[i].post_title + "</a></p><p><i class='fa fa-clock-o'></i> &nbsp;&nbsp;" + data[i].post_date + n_view + button
        ).hide().delay(i*225).fadeTo(450, 1);

        $child_div.append($info_div);
    }
}


// Function to load data from topyaps
function load_data (response, params, $div, page) {
    var data = [];

    $.ajax({
        url: 'topyaps_data/',
        type: "GET",
        data: {param: params},

        success: function(json) {
            if (!response) {
                for (var i=0; i<json.length; i++) {
                    data.push(json[i]);
                    data[i]["page"] = page
                }
            } else {
                for (var k=0; k<json.length; k++) {
                    for (var j=0; j<response.length; j++) {
                        if (json[k]["post_url"] == response[j]['link']) {
                            data.push({
                                'post_title': json[k]['post_title'],
                                'post_url': json[k]['post_url'],
                                'post_date': json[k]['post_date'],
                                'img_url': json[k]['img_url'],
                                'post_view': response[j]['view'],
                                'page': page
                            });
                        }
                    }
                }
            }
            data.sort(function(a,b) {return -(a.post_view - b.post_view)});
            createHTML(data, $div);
        },

        error: function(jqXhr) {
            var $alert_div = $("<div class='row col-lg-12' style='text-align:center'><div class='alert alert-danger'>Error retrieving data</div></div>");
            $div.children().remove();
            $div.append($alert_div);
            console.log(jqXhr.status + ": " + jqXhr.responseText);
        }
    });
}


// Function to load data for home page
function home_data($latest_div, $trending_div) {
    $.ajax({
        url: "realtime_data/",
        type: "GET",

        success: function(json) {
            load_data(null, "latest", $latest_div, "common");
            load_data(json, "all", $trending_div, "common");
        },

        error: function(jqXhr) {
            load_data(null, "latest", $latest_div, "common");
            var $alert_div = $("<div class='row col-lg-12' style='text-align:center'><div class='alert alert-danger'>Error retrieving Google data</div></div>");
            $trending_div.append($alert_div);
            console.log(jqXhr.status + ": " + jqXhr.responseText);

        }
    });
}


// Function to load page posts data
function view_data(page_id, $view_div) {
    var domain_url = window.location.href.split("/"),
        host_url = domain_url[0] + "//" + domain_url[2];

    $.ajax({
        url: host_url +'/publish_data/',
        type: "GET",
        data: {id: page_id},

        success: function(json) {
            if (json.length == 0) {
                var $alert_div = $("<div class='row col-lg-12' style='text-align:center'><div class='alert alert-danger'>First sync your data or post some articles on your page</div></div>");
                $view_div.empty().append($alert_div).hide().fadeIn(2000);
            } else {
                load_data(json, "all", $view_div, "view");
                console.log(json);
            }
        },

        error: function(jqXhr) {
            var $alert_div = $("<div class='row col-lg-12' style='text-align:center'><div class='alert alert-danger'>Error retrieving data from Database</div></div>");
            $view_div.empty().append($alert_div);
            console.log(jqXhr.status + ": " + jqXhr.responseText);
        }
    });
}


// Function get likes and talking about for each page
function additional_data(page_id, $like_div, $talking_div) {
    $.ajax({
        url: "additional_data/",
        type: "GET",
        data: {id: page_id},

        success: function(json) {
            $like_div.empty().append("<i class='fa fa-thumbs-up'></i>&nbsp;&nbsp;<span>" + json["likes"] + "</span>").hide().delay(200).fadeTo(400,1);
            $talking_div.empty().append("<i class='fa fa-users'></i>&nbsp;&nbsp;<span>" + json["talking_about_count"] + "</span>").hide().delay(200).fadeTo(400,1);
        },

        error: function (jqXhr) {
            $like_div.empty().append("<i class='fa fa-thumbs-up'></i>&nbsp;&nbsp;<span>NA</span>").hide().delay(200).fadeTo(400,1);
            $talking_div.empty().append("<i class='fa fa-users'></i>&nbsp;&nbsp;<span>NA</span>").hide().delay(200).fadeTo(400,1);
            console.log(jqXhr.status + ": " + jqXhr.responseText);
        }
    });
}



$(function() {
    var page_url = window.location.pathname;

    if (page_url == "/") {
        var $latest_div = $("#latest-data"),
            $trending_div = $("#trending-data");

        home_data($latest_div, $trending_div);
    } else if (page_url == "/account") {
        var $page_divs = $("[id=page-data]");

        $page_divs.each(function() {
            var $like_div = $(this).find("#likes"),
                $talking_div = $(this).find("#talking-about"),
                page_id = $(this).find("#sync-button").attr("value");

            additional_data(page_id, $like_div, $talking_div);
        });
    } else if (page_url.indexOf("published") >= 0) {
        var page_id = page_url.split('/')[2],
            $publish_div = $("#publish-data");

        view_data(page_id, $publish_div);
    }

    // Search function to load data on same page
    $("#search").on("submit", function(event) {
        event.preventDefault();

        var search_term = $("#q").val(),
            $search_div = $("#search-data"),
            $loading_div = $("<div class='col-lg-12' style='text-align: center'><div class='alert alert-info'>Searching for: "
                + search_term + "&nbsp;&nbsp;<i class='fa fa-spinner fa-spin'></i> </div></div>");

        $search_div.empty();

        if (!search_term) {
            var $empty_div = $("<div class='col-lg-12' style='text-align: center'><div class='alert alert-danger'>Input search string</div></div>");
            $search_div.append($empty_div).fadeOut(3000, function() {
                $empty_div.remove();
            }).fadeIn(1000);
        } else {
            $search_div.append($loading_div);
            load_data(null, "search&search_text=" + search_term, $search_div, "common");
        }
    });
});
