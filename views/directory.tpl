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

<h1> Choose the game you're participating in</h1>
% for game_id, game_name in games.iteritems():
  <a href="/{{ game_id }}"><h3>{{ game_name }}</h3></a>
% end

</div>
</body>
</html>
