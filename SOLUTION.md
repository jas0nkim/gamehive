Create Database

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

