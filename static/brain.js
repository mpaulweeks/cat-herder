
function setUpListeners(weekId){
    // ajax goes here
    $('.vote').click(function (){
        var $this = $(this);
        $this.toggleClass("True");
    });
    $('.save').click(function (){
        var $this = $(this);
        var pid = $this.data('pid');
        var event_ids = [];
        $('.vote.True.pid-' + pid).each(function (){
            var $elm = $(this);
            event_ids.push($elm.data('event'));
        });
        var data = {
            "new_name": $('#pid-' + pid).val(),
            "event_ids": event_ids
        };
        $.ajax({
            url: '/event/' + weekId + '/participant/' + pid,
            type: 'PUT',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data),
        }).done(function (data){
            location.reload();
        }).fail(function (data){
            alert('something broke');
        });
    });
}
