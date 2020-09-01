## Production level quality

- Structured python package
- Nginx + Gunicon web server
- Hide sensitive information (ie. database access)
- Persist production data

## Build servers with Docker Compose

```
$ docker-compose up -d
```

## Build database tables

WARNING: run following will remove existing data in the tables - players, guilds, items, player_items
```
$ docker exec -ti gamehive_appserver_1 python
Python 3.6.12 (default, Aug 18 2020, 04:36:04)
[GCC 6.3.0 20170516] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from app import init_db
>>> init_db()
```

## API endpoints

### Players
```
/player
    1. GET: list players
    2. POST: create new player
/player/<nickname>
    1. GET: show player
    2. POST or PUT: update existing player
/player/<nickname>/delete
    1. POST or DELETE: delete player
/player/<nickname>/add-item
    1. POST: add an item to a player
/player/<nickname>/remove-item/<itemname>
    1. POST or DELETE: remove an item from a player
/player/<nickname>/join-guild
    1. POST: join a player into a guild
/player/<nickname>/leave-guild
    1. POST: leave from a joined guild
```

### Guilds
```
/guild
    1. GET: list guilds
    2. POST: create new guild
/guild/<name>
    1. GET: show guild. show joined players
    2. POST or PUT: update existing guild
/guild/<name>/delete
    1. POST or DELETE: delete guild
/guild/<name>/add-player
    1. POST: add player
/guild/<name>/remove-player/<nickname>
    1. POST: remove player
/guild/<name>/points
    1. GET: get the total number of skill points in a guild
```

### Items
```
/item
    1. GET: list items
    2. POST: create new item
/item/<name>
    1. GET: show item
    2. POST or PUT: update existing item
/item/<name>/delete
    1. POST or DELETE: delete item
```

## Access API

The API can be accessed via port `9999`. You may change it from `services` > `nginx` > `ports` in `docker-compose.yml`

## Run tests & coverage

```
$ docker exec -ti gamehive_appserver_1 pytest --cov=gamehiveplayer tests
```

## Hide sensitive information

Remove `.config` directory from the git repository by adding line in `.gitignore`
```
.config/
```