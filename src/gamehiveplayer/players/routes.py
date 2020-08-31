from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from gamehiveplayer.models import Player, db

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
        player = Player(nickname=req_data['nickname'], email=req_data['email'])
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
            p.nickname = req_data['nickname']
            p.email = req_data['email']
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

