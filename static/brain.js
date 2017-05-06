
function setUpListeners(gameId, weekId){
    var admin = false;

    var _pids = new Set();
    $('.name-view').each(function (){
        var pid = $(this).data('pid');
        _pids.add(pid);
    });

    function encodePid(pid){
        return pid.replace("/", "%2F");
    }
    function $pid(pid, query){
        return $(query + '*[data-pid="' + pid + '"]');
    }
    function genDeleteRequest(pid){
        var requestUrl = (
            '/game/' + gameId +
            '/event/' + weekId +
            '/participant/' + encodePid(pid)
        )
        return {
            url: encodeURI(requestUrl),
            type: 'DELETE',
            contentType: 'charset=utf-8',
        }
    }
    function genSaveRequest(pid, data){
        var requestType = 'POST';
        var requestUrl = (
            '/game/' + gameId +
            '/event/' + weekId +
            '/participant'
        )
        if (pid != ""){
            requestType = 'PUT';
            requestUrl += '/' + encodePid(pid)
        }
        return {
            url: encodeURI(requestUrl),
            type: requestType,
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data),
        }
    }
    function genChosenRequest(eventId){
        var requestUrl = (
            '/game/' + gameId +
            '/event/' + weekId +
            '/chosen/' + eventId
        )
        return {
            url: encodeURI(requestUrl),
            type: 'PUT',
            contentType: 'application/json; charset=utf-8',
        }
    }
    function checkValidName(pid, new_name){
        if (new_name == ""){
            alert("must enter a name");
            return false;
        }
        if (pid != new_name){
            if (_pids.has(new_name)){
                alert("must enter a unique name");
                return false;
            }
        }
        return true;
    }
    function toggleAdmin(){
        admin = !admin;
        if (admin){
            $('.header-time div').addClass("clickable");
            $('.header-time a').removeClass("hidden");
        } else {
            $('.header-time div').removeClass("clickable");
            $('.header-time a').addClass("hidden");
        }
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
        if (!checkValidName(pid, new_name)){
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
        $.ajax(
            genSaveRequest(pid, data)
        ).done(function (data){
            location.reload();
        }).fail(function (data){
            alert('something broke');
        });
    });
    $('.delete').click(function (){
        var $this = $(this);
        var pid = $this.data('pid');
        $.ajax(
            genDeleteRequest(pid)
        ).done(function (data){
            location.reload();
        }).fail(function (data){
            alert('something broke');
        });
    });
    $('.header-time div').click(function(e){
        if (!admin){
            return;
        }
        var $this = $(this);
        var eventId = $this.data('id');
        $.ajax(
            genChosenRequest(eventId)
        ).done(function (data){
            location.reload();
        }).fail(function (data){
            alert('something broke');
        });
    })

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
        if (pid == ""){
            $pid(pid, '.delete').hide();
        }
    }

    $('.edit').click(function (){
        var $this = $(this);
        var pid = $this.data('pid');
        updateView(pid, true);
    });
    $('#toggle-highlight').click(function (){
        toggleAdmin();
    });
    $("body").keypress(function( event ) {
        if ( event.which == 96 ) {
            // `
            event.preventDefault();
            toggleAdmin();
        }
    });

    function hover(event){
        var query = ".col-" + $(this).data("id");
        if ($(this).hasClass('highlight')){
            query = '.highlight' + query;
        } else if ($(this).hasClass('highlight-header')) {
            query = '.highlight-header' + query;
        } else {
            return;
        }
        if (event.type == 'mouseover') {
            // $(this).parent().addClass("hover");
            $(query).addClass("hover");
        }
        else {
            $(query).removeClass("hover");
        }
    }
    $("table").delegate('th','mouseover mouseleave',hover);
    $("table").delegate('td','mouseover mouseleave',hover);
}
