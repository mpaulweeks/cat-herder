<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Cat Herder</title>
<link rel='shortcut icon' type='image/x-icon' href='static/favicon.ico' />
<meta name="viewport" content="width=device-width, initial-scale=1">

<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" integrity="sha256-7s5uDGW3AHqw6xtJmNNtr+OBRJUlgkNJEo78P4b0yRw= sha512-nNo+yCHEyn0smMxSswnf/OnX6/KwJuZTlNZBjauKhTK0c+zT+q5JOCx0UFhXQ6rJR9jg6Es8gPuD2uZcYDLqSw==" crossorigin="anonymous">
<link rel="stylesheet" href="/static/style.css">

<script src="https://code.jquery.com/jquery-1.12.0.min.js"> </script>
<script src="/static/brain.js"> </script>

</head>
<body>

<div class="container text-center">

<h1> {{ data.game_name }} Scheduler </h1>
<h3> Today is {{ today.strftime("%A, %B %d") }} </h3>
% if data.id > "20160808":
  <h4> Looking for <a href="/{{data.game_id}}/{{last_week_id}}">lask week?</a> </h4>
% end

<table class="table" id="dates">
<thead>
  <tr class="top">
    <th></th>
    % for date in data.event_dates:
    <th colspan="{{ len(date.times) }}"><div>
      {{ date.dayName }} <br/> {{ date.name }}
    </div></th>
    % end
    <th></th>
  </tr>
  <tr class="bottom">
    <th></th>
    % for date in data.event_dates:
    % for time in date.times:
    <th class="highlight"><div>
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
        <td class="{{ 'highlight' if person.name else '' }}">
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
  var gameId = "{{ data.game_id }}";
  var weekId = "{{ data.id }}";
  setUpListeners(gameId, weekId);
});
</script>
</body>
</html>
