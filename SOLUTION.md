## Database

```
$ docker exec -ti gamehive_appserver_1 python
Python 3.6.12 (default, Aug 18 2020, 04:36:04)
[GCC 6.3.0 20170516] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from gamehiveplayer import create_app
>>> from gamehiveplayer.models import db
>>> app = create_app()
>>> with app.app_context():
...    db.create_all()
...
>>>
```

## API Endpoints

### Player

```
/player
    1. GET: list players
    2. POST: create new player
/player/<UUID>
    1. GET: show player
    2. POST or PUT: update existing player
/player/<UUID>/delete
    1. POST or DELETE: delete player
/player/<UUID>/add-item
    1. POST: add an item to a player
/player/<UUID>/join
    1. POST: join a player into a guild
/player/<UUID>/leave
    1. POST: leave from a joined guild
```

### Guild

```
/guild
    1. GET: list guilds
    2. POST: create new guild
/guild/<UUID>
    1. GET: show guild. show joined players
    2. POST or PUT: update existing guild
/guild/<UUID>/delete
    1. POST or DELETE: delete guild
/guild/<UUID>/add-player
    1. POST: add player
/guild/<UUID>/remove-player
    1. POST: remove player
/guild/<UUID>/points
    1. GET: calculate the total number of skill points in a guild
```

### Item

```
/item
    1. GET: list guilds
    2. POST: create new guild
/item/<UUID>
    1. GET: show guild
    2. POST or PUT: update existing guild
/item/<UUID>/delete
    1. POST or DELETE: delete guild
```

## Test & Coverage

```
$ docker exec -ti gamehive_appserver_1 /bin/bash
root@3f2783ae7350:/src# pytest --cov=gamehiveplayer tests
```
