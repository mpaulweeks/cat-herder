<!DOCTYPE html>
<html lang="en">
<head>
<title>Cat Herder</title>

% include('_header.tpl')

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
