jQuery.ajaxSettings.traditional = true;
$(document).ready(function () {
    $("#scan_button").addClass("loading");
    populate_hosts();
    $("#scan_button").click(function(){
        $("#scan_button").addClass("loading");
        $('#net_view_body').empty()
        populate_hosts();
    });
});

hosts_global = []

function populate_hosts(){
    $.getJSON("/hosts",{},function(hosts){
        $.each(hosts, function(index, val){
            let id = Math.random().toString(36).substring(7);
            $('#net_view_table').append('<tr><td>'+index+'</td><<td>'+hosts[index]+'</td><td style="height:100%"><a class="ui toggle button" style="width: 100%; height:100%" id="'+id+'">Deauth</a></td></tr>');
            $('#'+id).click(function(){
                $.post("/deauth", {target: index}, function(data, status){
                    alert("deauth attack on " + host)
                })
            });

        });
        $("#scan_button").removeClass("loading");
    });
}
