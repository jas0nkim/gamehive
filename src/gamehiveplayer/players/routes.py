from flask import Blueprint, request, jsonify
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
        return jsonify(success='true')
    elif request.method == 'POST':
        req_data = request.get_json()
        if not req_data:
            return jsonify(success='false', error_message='mimetype does not indicate JSON')

        player = Player(nickname=req_data['nickname'], email=req_data['email'])
        db.session.add(player)
        db.session.commit()
        return jsonify(success='true')
    else:
        return jsonify(success='false', error_message='only HTTP POST method allowed.')

@players.route('/player/<id>/update', methods=['POST', 'PUT'])
def update_player(id):
    """ POST method:
            update existing player
            return json
                eg.
                {
                    'success': 'true'
                }
    """
    if request.method != 'POST':
        return jsonify(success='false', error_message='only HTTP POST method allowed.')
    
    req_data = request.get_json()
    if not req_data:
        return jsonify(success='false', error_message='mimetype does not indicate JSON')

    player = Player(nickname=req_data['nickname'], email=req_data['email'])
    db.session.add(player)
    db.session.commit()
    return jsonify(success='true')
