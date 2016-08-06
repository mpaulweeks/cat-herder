<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Cat Herder</title>
<link rel='shortcut icon' type='image/x-icon' href='static/favicon.ico' />
<meta name="viewport" content="width=device-width, initial-scale=1">

<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" integrity="sha256-7s5uDGW3AHqw6xtJmNNtr+OBRJUlgkNJEo78P4b0yRw= sha512-nNo+yCHEyn0smMxSswnf/OnX6/KwJuZTlNZBjauKhTK0c+zT+q5JOCx0UFhXQ6rJR9jg6Es8gPuD2uZcYDLqSw==" crossorigin="anonymous">
<link rel="stylesheet" href="static/style.css">

<script src="https://code.jquery.com/jquery-1.12.0.min.js"> </script>
<script src="static/brain.js"> </script>

</head>
<body>

<div class="container text-center">

<table class="table" id="dates">
<thead>
  <tr>
    <th></th>
    % for date in data.event_dates:
    <th colspan="{{ len(date.times) }}"><div class="col-header">
      {{ date.name }}
    </div></th>
    % end
  </tr>
</thead>
<tbody>
% for person in participants:
  <tr>
  <td>
    <input value="{{ person.name or '' }}" placeholder="(your name here)">
    <button class="save" data-pid="{{person.name}}">SAVE</button>
  </td>
    % for date in data.event_dates:
    % for time in date.times:
        <td><div class="clickable vote {{'True' if person.get(time) else ''}} pid-{{person.name}}" data-event="{{time.event_id}}">
          {{ time.name }}
        </div></td>
    % end
    % end
  </tr>
% end
</tbody>
</table>

<button id="submit"> UPDATE </button>

</div>
<script type="text/javascript">
$(document).ready(function () {
  var weekId = "{{ data.id }}";
  setUpListeners(weekId);
});
</script>
</body>
</html>
