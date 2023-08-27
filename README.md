# TicTacToe-Django

Game TicTacToe in Django

## Index
- [Deploy](#deploy)
- [Login](#majority-element)
- [Create Match](#create-match)
- [Join Match](#join-match)
- [Play Match](#play-match)
- [Detail Match](#detail-match)
- [Statistics](#statistics)


### Deploy

This application is prepared with **Docker**. We have two components, the application and the database. Just Run
```
 docker-compose up
 ```

### Login

Request
```
curl --location 'http://localhost:8000/users_app/login/' \
--form 'username="player1"' \
--form 'password="contra1234"'
```

Response
```
{
  "token": "xxxx"
}
```

### Create Match

Request
```
curl --location --request POST 'http://localhost:8000/tictactoe_app/match-create/' \
--header 'Authorization: Token xxxx'
```

Response
```
{
  "id": 2
}
```

### Join Match
Request
```
curl --location --request POST 'http://localhost:8000/tictactoe_app/match-join/2/' \
--header 'Authorization: Token xxxx'
```

Response
```
200 OK
```

### Play Match

Request
```
curl --location --request POST 'http://localhost:8000/tictactoe_app/match-play/1/' \
--header 'Authorization: Token xxxx'
```

Response
```
200 OK
```

### Detail Match


Request
```
curl --location 'http://localhost:8000/tictactoe_app/match-detail/1/' \
--header 'Authorization: Token xxxx'
```

Response
```
{
    "id": 1,
    "X": "player1",
    "O": "player2",
    "turn": 10,
    "finish": true,
    "winner": "player1",
    "board_row0": "X | O | O",
    "board_row1": "O | X | X",
    "board_row2": "- | O | X"
}
```

### Statistics

Request
```
curl --location 'http://localhost:8000/tictactoe_app/matches-statistics/' \
--header 'Authorization: Token xxxx'
```

Response
```
{
    "wins": 1,
    "draws": 0,
    "loses": 0,
    "total_matches_finish": 1,
    "list_matches_finish": [1],
    "total_matches_unfinish": 0,
    "list_matches_unfinish": []
}
```
 
