from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from gamehiveplayer.models import Player, Item, Guild, db

players = Blueprint('players', __name__)


@players.route('/player', methods=['GET', 'POST'])
def list_or_create_player():
    """ GET method:
            list players
            return json
                eg.
                {
                    'success': 'true',
                    'players': [
                        ...
                    ]
                }
        POST method:
            create new player
            return json
                eg.
                {
                    'success': 'true'
                }
    """
    if request.method == 'GET':
        return jsonify(success='true', players=[p.as_dict() for p in Player.query.all()]), 200
    elif request.method == 'POST':
        req_data = request.get_json()
        if not req_data:
            return jsonify(success='false', error_message='mimetype does not indicate JSON'), 404
        player = Player(nickname=req_data.get('nickname'), email=req_data.get('email'))
        db.session.add(player)
        try:
            db.session.commit()
        except IntegrityError as e:
            return jsonify(success='false', error_message=repr(e)), 400
        else:
            return jsonify(success='true'), 201
    else:
        return jsonify(success='false', error_message='only HTTP POST method allowed.'), 405

@players.route('/player/<nickname>', methods=['GET', 'POST', 'PUT'])
def update_player(nickname):
    """ GET method:
            show player
            return json
                eg.
                {
                    'success': 'true',
                    'player': {
                        'nickname': 'test02',
                        'email': 'test02@mail.com'
                    }
                }
        POST or PUT method:
            update existing player
            return json
                eg.
                {
                    'success': 'true'
                }
    """
    if request.method == 'GET':
        p = Player.query.filter_by(nickname=nickname).first()
        if p is None:
            return jsonify(success='false', error_message='Not found'), 404
        else:
            return jsonify(success='true', player=p.as_dict()), 200
    elif request.method in ['POST', 'PUT']:
        p = Player.query.filter_by(nickname=nickname).first()
        if p is None:
            return jsonify(success='false', error_message='Not found'), 404
        else:
            req_data = request.get_json()
            p.nickname = req_data.get('nickname')
            p.email = req_data.get('email')
            try:
                db.session.commit()
            except IntegrityError as e:
                return jsonify(success='false', error_message=repr(e)), 400
            else:
                return jsonify(success='true'), 200
    else:
        return jsonify(success='false', error_message='only HTTP GET/POST/PUT method allowed.'), 405

@players.route('/player/<nickname>/delete', methods=['DELETE', 'POST'])
def delete_player(nickname):
    """ DELETE or POST method:
            delete a player
            return json
                eg.
                {
                    'success': 'true'
                }
    """
    if request.method in ['DELETE', 'POST']:
        p = Player.query.filter_by(nickname=nickname).first()
        if p is None:
            return jsonify(success='false', error_message='Not found'), 404
        else:
            db.session.delete(p)
            try:
                db.session.commit()
            except IntegrityError as e:
                return jsonify(success='false', error_message=repr(e)), 400
            else:
                return jsonify(success='true'), 200
    else:
        return jsonify(success='false', error_message='only HTTP DELETE/POST method allowed.'), 405

@players.route('/player/<nickname>/add-item', methods=['POST'])
def add_item_to_player(nickname):
    """ POST method:
            add an item to a player
            return json
                eg.
                {
                    'success': 'true',
                    'items': [
                        ...
                    ]
                }
    """
    if request.method in ['POST']:
        p = Player.query.filter_by(nickname=nickname).first()
        if p is None:
            return jsonify(success='false', error_message='Not found'), 404
        else:
            req_data = request.get_json()
            if not req_data:
                return jsonify(success='false', error_message='Item not found'), 400
            i = Item.query.filter_by(name=req_data.get('name')).first()
            if i is None:
                return jsonify(success='false', error_message='Item not found'), 400
            if i in p.items:
                return jsonify(success='false', error_message='Item already exists to the player.'), 400
            p.items.append(i)
            try:
                db.session.commit()
            except IntegrityError as e:
                return jsonify(success='false', error_message=repr(e)), 400
            else:
                return jsonify(success='true', items=[j.as_dict() for j in p.items]), 200
    else:
        return jsonify(success='false', error_message='only HTTP POST method allowed.'), 405

@players.route('/player/<nickname>/remove-item/<itemname>', methods=['DELETE', 'POST'])
def delete_item_from_player(nickname, itemname):
    """ DELETE or POST method:
            delete an item from a player
            return json
                eg.
                {
                    'success': 'true',
                    'items': [
                        ...
                    ]
                }
    """
    if request.method in ['DELETE', 'POST']:
        p = Player.query.filter_by(nickname=nickname).first()
        if p is None:
            return jsonify(success='false', error_message='Not found'), 404
        else:
            i = Item.query.filter_by(name=itemname).first()
            if i is None:
                return jsonify(success='false', error_message='Item not found'), 400
            if i not in p.items:
                return jsonify(success='false', error_message='Player does not have the item.'), 400
            p.items.remove(i)
            try:
                db.session.commit()
            except IntegrityError as e:
                return jsonify(success='false', error_message=repr(e)), 400
            else:
                return jsonify(success='true', items=[j.as_dict() for j in p.items]), 200
    else:
        return jsonify(success='false', error_message='only HTTP DELETE/POST method allowed.'), 405

@players.route('/player/<nickname>/join-guild', methods=['POST'])
def join_player_to_guild(nickname):
    """ POST method:
            join a player into a guild
            return json
                eg.
                {
                    'success': 'true',
                    'player': {
                        ...
                    }
                }
    """
    if request.method in ['POST']:
        p = Player.query.filter_by(nickname=nickname).first()
        if p is None:
            return jsonify(success='false', error_message='Not found'), 404
        else:
            req_data = request.get_json()
            if not req_data:
                return jsonify(success='false', error_message='Guild not found'), 400
            g = Guild.query.filter_by(name=req_data.get('name')).first()
            if g is None:
                return jsonify(success='false', error_message='Guild not found'), 400
            p.guild_id = g.id
            try:
                db.session.commit()
            except IntegrityError as e:
                return jsonify(success='false', error_message=repr(e)), 400
            else:
                return jsonify(success='true', player=p.as_dict()), 200
    else:
        return jsonify(success='false', error_message='only HTTP POST method allowed.'), 405

@players.route('/player/<nickname>/leave-guild', methods=['POST'])
def leave_player_from_guild(nickname):
    """ POST method:
            leave from a joined guild
            return json
                eg.
                {
                    'success': 'true',
                    'player': {
                        ...
                    }
                }
    """
    if request.method in ['POST']:
        p = Player.query.filter_by(nickname=nickname).first()
        if p is None:
            return jsonify(success='false', error_message='Not found'), 404
        else:
            p.guild_id = None
            try:
                db.session.commit()
            except IntegrityError as e:
                return jsonify(success='false', error_message=repr(e)), 400
            else:
                return jsonify(success='true', player=p.as_dict()), 200
    else:
        return jsonify(success='false', error_message='only HTTP POST method allowed.'), 405
