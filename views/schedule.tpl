<!DOCTYPE html>
<html lang="en">
<head>
<title>Cat Herder - {{ data.game.name }}</title>

% include('_header.tpl', epoch=epoch)

<script src="/static/brain.js?version={{ epoch }}"> </script>

</head>
<body>

<div class="hidden-link">
  <a href="/{{ next_game.id }}/{{ data.id }}">S</a>
</div>
<div id="toggle-highlight" class="hidden-link right clickable">
  A
</div>

<div class="container text-center">
<h3 class="admin-alert hidden"> ADMIN ENABLED </h3>
<h1> {{ data.game.name }} Scheduler </h1>
<h4> {{ data.game.subtitle }} </h4>
% if data.message:
  <h4 class="message"> {{ data.message }} </h4>
% end
<h3> Today is {{ today.strftime("%A, %B %d") }} </h3>
% if last_week_id and next_week_id:
  <h4> Looking for <a href="/{{data.game.id}}/{{last_week_id}}">last week</a> or <a href="/{{data.game.id}}/{{next_week_id}}">next week</a>? </h4>
% elif last_week_id:
  <h4> Looking for <a href="/{{data.game.id}}/{{last_week_id}}">last week</a>? </h4>
% elif next_week_id:
  <h4> Looking for <a href="/{{data.game.id}}/{{next_week_id}}">next week</a>? </h4>
% end

<table class="table" id="dates">
<thead>
  <tr class="top">
    <th></th>
    % for date in data.event_dates:
    <th class="highlight highlight-header {{date.col_css(data)}}" colspan="{{ len(date.times) }}"><div>
      {{ date.dayName }} <br/> {{ date.name }}
    </div></th>
    % end
    <th></th>
  </tr>
  <tr class="bottom">
    <th></th>
    % for date in data.event_dates:
    % for time in date.times:
    <th class="highlight highlight-header header-time {{time.col_css(data)}}">
      % if time.is_chosen(data):
        <a class="hidden" href="{{ time.gcal(data.game) }}" target="_blank"> GCAL </a>
      % end
      <div data-id="{{time.event_id}}"> {{ time.name }} </div>
    </th>
    % end
    % end
    <th></th>
  </tr>
</thead>
<tbody>
% for person in participants:
  <tr>
  <td>
    <div {{person.is_old}} class="name-view" data-pid="{{person.id}}">{{person.name}}</div>
    <input {{person.is_new}} value="{{ person.name }}" placeholder="(your name here)" class="name-edit" data-pid="{{person.id}}">
  </td>
    % for date in data.event_dates:
    % for time in date.times:
        <td class="{{ 'highlight' if person.name else 'highlight-header' }} {{time.col_css(data)}}" data-id="{{time.event_id}}">
        <div class="{{person.clickable}} vote {{'True' if person.get(time) else ''}}" data-event="{{time.event_id}}" data-pid="{{person.id}}">
          <!-- nothing, filled with css -->
        </div>
        </td>
    % end
    % end
  <td>
    <button {{person.is_old}} class="edit" data-pid="{{person.id}}">EDIT</button>
    <button {{person.is_new}} class="save" data-pid="{{person.id}}">SAVE</button>
    <button style="display: none;" class="delete" data-pid="{{person.id}}">DELETE</button>
  </td>
  </tr>
% end
</tbody>
</table>

</div>
<script type="text/javascript">
$(document).ready(function () {
  var gameId = "{{ data.game.id }}";
  var weekId = "{{ data.id }}";
  setUpListeners(gameId, weekId);
});
</script>
</body>
</html>
