
function setUpListeners(weekId){
    function $pid(pid, query){
        return $(query + '*[data-pid="' + pid + '"]');
    }

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
        var new_name = $pid(pid, '.name-edit').val();
        if (new_name == ""){
            alert("must enter a name");
            return;
        }
        var event_ids = [];
        $pid(pid, '.vote.True').each(function (){
            var $elm = $(this);
            event_ids.push($elm.data('event'));
        });
        var data = {
            "new_name": new_name,
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
    $('.delete').click(function (){
        var $this = $(this);
        var pid = $this.data('pid');
        $.ajax({
            url: '/event/' + weekId + '/participant/' + pid,
            type: 'DELETE',
            contentType: 'charset=utf-8',
        }).done(function (data){
            location.reload();
        }).fail(function (data){
            alert('something broke');
        });
    });

    function updateView(pid, canEdit){
        if (canEdit){
            $pid(pid, '.name-view').hide();
            $pid(pid, '.name-edit').show();
            $pid(pid, '.edit').hide();
            $pid(pid, '.save').show();
            $pid(pid, '.delete').show();
            $pid(pid, '.vote').addClass('clickable');
        } else {
            $pid(pid, '.name-view').show();
            $pid(pid, '.name-edit').hide();
            $pid(pid, '.edit').show();
            $pid(pid, '.save').hide();
            $pid(pid, '.delete').hide();
            $pid(pid, '.vote').removeClass('clickable');
        }
        if (pid == "None"){
            $pid(pid, '.delete').hide();
        }
    }

    $('.edit').click(function (){
        var $this = $(this);
        var pid = $this.data('pid');
        updateView(pid, true);
    });
}
