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
    % for time in date.times:
        <th>{{ time.name }}</th>
    % end
    % end
  </tr>
</thead>
<tbody>
% for person in participants:
  <tr>
  <td>{{ person.name or "n/a" }}</td>
    % for date in data.event_dates:
    % for time in date.times:
        <td>{{ str(person.get(time)) }}</td>
    % end
    % end
  </tr>
% end
</tbody>
</table>

</div>
<script type="text/javascript">
$(document).ready(function () {
    setUpListeners();
});
</script>
</body>
</html>
