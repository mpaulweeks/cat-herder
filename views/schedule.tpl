<!DOCTYPE html>
<html lang="en">
<head>
<title>Cat Herder - {{ data.game.name }}</title>

% include('_header.tpl')

<script src="/static/brain.js"> </script>

</head>
<body>

<div class="hidden-link">
  <a href="/{{ next_game.id }}/{{ data.id }}">-></a>
</div>

<div class="container text-center">

<h1> {{ data.game.name }} Scheduler </h1>
<h4> {{ data.game.subtitle }} </h4>
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
    <th class="highlight highlight-header {{date.col_css}}" colspan="{{ len(date.times) }}"><div>
      {{ date.dayName }} <br/> {{ date.name }}
    </div></th>
    % end
    <th></th>
  </tr>
  <tr class="bottom">
    <th></th>
    % for date in data.event_dates:
    % for time in date.times:
    <th class="highlight highlight-header {{time.col_css}}" data-id="{{time.event_id}}"><div>
      {{ time.name }}
    </div></th>
    % end
    % end
    <th></th>
  </tr>
</thead>
<tbody>
% for person in participants:
  <tr>
  <td>
    <div {{person.is_old}} class="name-view" data-pid="{{person.name}}">{{person.name}}</div>
    <input {{person.is_new}} value="{{ person.name }}" placeholder="(your name here)" class="name-edit" data-pid="{{person.name}}">
  </td>
    % for date in data.event_dates:
    % for time in date.times:
        <td class="{{ 'highlight' if person.name else 'highlight-header' }} {{time.col_css}}" data-id="{{time.event_id}}">
        <div class="{{person.clickable}} vote {{'True' if person.get(time) else ''}}" data-event="{{time.event_id}}" data-pid="{{person.name}}">
          <!-- nothing, filled with css -->
        </div>
        </td>
    % end
    % end
  <td>
    <button {{person.is_old}} class="edit" data-pid="{{person.name}}">EDIT</button>
    <button {{person.is_new}} class="save" data-pid="{{person.name}}">SAVE</button>
    <button style="display: none;" class="delete" data-pid="{{person.name}}">DELETE</button>
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
