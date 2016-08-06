
function setUpListeners(weekId){
    $('.vote').click(function (){
        var $this = $(this);
        if (!$this.hasClass("clickable")){
            return;
        }
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
            "new_name": $('.name-edit.pid-' + pid).val(),
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
    // todo add DELETE ajax

    function updateView(pid, canEdit){
        if (canEdit){
            $('.name-view.pid-' + pid).hide();
            $('.name-edit.pid-' + pid).show();
            $('.edit.pid-' + pid).hide();
            $('.save.pid-' + pid).show();
            $('.vote.pid-' + pid).addClass('clickable');
        } else {
            $('.name-view.pid-' + pid).show();
            $('.name-edit.pid-' + pid).hide();
            $('.edit.pid-' + pid).show();
            $('.save.pid-' + pid).hide();
            $('.vote.pid-' + pid).removeClass('clickable');
        }
    }

    $('.edit').click(function (){
        var $this = $(this);
        var pid = $this.data('pid');
        updateView(pid, true);
    });

    $('.name-edit').each(function (){
        var $this = $(this);
        var pid = $this.data('pid');
        var canEdit = $this.val() == "";
        updateView(pid, canEdit);
    });
}
