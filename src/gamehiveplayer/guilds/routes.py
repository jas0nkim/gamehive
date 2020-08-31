from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from gamehiveplayer.models import Guild, Player, db
from gamehiveplayer.guilds.utils import calculate_total_skill_points

guilds = Blueprint('guilds', __name__)

@guilds.route('/guild', methods=['GET', 'POST'])
def list_or_create_guild():
    """ GET method:
            list guilds
            return json
                eg.
                {
                    'success': 'true',
                    'guilds': [
                        ...
                    ]
                }
        POST method:
            create new guild
            return json
                eg.
                {
                    'success': 'true'
                }
    """
    if request.method == 'GET':
        return jsonify(success='true', guilds=[g.as_dict() for g in Guild.query.all()]), 200
    elif request.method == 'POST':
        req_data = request.get_json()
        if not req_data:
            return jsonify(success='false', error_message='mimetype does not indicate JSON'), 404
        guild = Guild(name=req_data.get('name'), country_code=req_data.get('country_code'))
        db.session.add(guild)
        try:
            db.session.commit()
        except IntegrityError as e:
            return jsonify(success='false', error_message=repr(e)), 400
        else:
            return jsonify(success='true'), 201
    else:
        return jsonify(success='false', error_message='only HTTP POST method allowed.'), 405

@guilds.route('/guild/<name>', methods=['GET', 'POST', 'PUT'])
def update_guild(name):
    """ GET method:
            show guild
            return json
                eg.
                {
                    'success': 'true',
                    'guild': {
                        'name': 'testguild02',
                        'country_code': 'US'
                    }
                }
        POST or PUT method:
            update existing guild
            return json
                eg.
                {
                    'success': 'true'
                }
    """
    if request.method == 'GET':
        g = Guild.query.filter_by(name=name).first()
        if g is None:
            return jsonify(success='false', error_message='Not found'), 404
        else:
            return jsonify(success='true', guild=g.as_dict()), 200
    elif request.method in ['POST', 'PUT']:
        g = Guild.query.filter_by(name=name).first()
        if g is None:
            return jsonify(success='false', error_message='Not found'), 404
        else:
            req_data = request.get_json()
            g.name = req_data.get('name')
            g.country_code = req_data.get('country_code')
            try:
                db.session.commit()
            except IntegrityError as e:
                return jsonify(success='false', error_message=repr(e)), 400
            else:
                return jsonify(success='true'), 200
    else:
        return jsonify(success='false', error_message='only HTTP GET/POST/PUT method allowed.'), 405

@guilds.route('/guild/<name>/delete', methods=['DELETE', 'POST'])
def delete_guild(name):
    """ DELETE or POST method:
            delete a guild
            return json
                eg.
                {
                    'success': 'true'
                }
    """
    if request.method in ['DELETE', 'POST']:
        g = Guild.query.filter_by(name=name).first()
        if g is None:
            return jsonify(success='false', error_message='Not found'), 404
        else:
            db.session.delete(g)
            try:
                db.session.commit()
            except IntegrityError as e:
                return jsonify(success='false', error_message=repr(e)), 400
            else:
                return jsonify(success='true'), 200
    else:
        return jsonify(success='false', error_message='only HTTP DELETE/POST method allowed.'), 405

@guilds.route('/guild/<name>/add-player', methods=['POST'])
def add_player_to_guild(name):
    """ POST method:
            add player to a guild
            return json
                eg.
                {
                    'success': 'true',
                    'players': [
                        ...
                    ]
                }
    """
    if request.method in ['POST']:
        g = Guild.query.filter_by(name=name).first()
        if g is None:
            return jsonify(success='false', error_message='Not found'), 404
        else:
            req_data = request.get_json()
            if not req_data:
                return jsonify(success='false', error_message='Player not found.'), 400
            p = Player.query.filter_by(nickname=req_data.get('nickname')).first()
            if p is None:
                return jsonify(success='false', error_message='Player not found.'), 400
            if p in g.players:
                return jsonify(success='false', error_message='Player already joined.'), 400
            g.players.append(p)
            try:
                db.session.commit()
            except IntegrityError as e:
                return jsonify(success='false', error_message=repr(e)), 400
            else:
                return jsonify(success='true', players=[pl.as_dict() for pl in g.players]), 200
    else:
        return jsonify(success='false', error_message='only HTTP POST method allowed.'), 405

@guilds.route('/guild/<name>/remove-player/<nickname>', methods=['DELETE', 'POST'])
def remove_player_from_guild(name, nickname):
    """ DELETE or POST method:
            remove player from a guild
            return json
                eg.
                {
                    'success': 'true',
                    'players': [
                        ...
                    ]
                }
    """
    if request.method in ['DELETE', 'POST']:
        g = Guild.query.filter_by(name=name).first()
        if g is None:
            return jsonify(success='false', error_message='Not found'), 404
        else:
            p = Player.query.filter_by(nickname=nickname).first()
            if p is None:
                return jsonify(success='false', error_message='Player not found.'), 400
            if p not in g.players:
                return jsonify(success='false', error_message='Player not a member.'), 400
            g.players.remove(p)
            try:
                db.session.commit()
            except IntegrityError as e:
                return jsonify(success='false', error_message=repr(e)), 400
            else:
                return jsonify(success='true', players=[pl.as_dict() for pl in g.players]), 200
    else:
        return jsonify(success='false', error_message='only HTTP DELETE/POST method allowed.'), 405

@guilds.route('/guild/<name>/points', methods=['GET'])
def total_skill_points(name):
    """ GET method:
            get the total number of skill points in a guild
            return json
                eg.
                {
                    'success': 'true',
                    'total_points': ...
                }
    """
    if request.method in ['GET']:
        g = Guild.query.filter_by(name=name).first()
        if g is None:
            return jsonify(success='false', error_message='Not found'), 404
        else:
            return jsonify(success='true', total_points=calculate_total_skill_points(g)), 200
    else:
        return jsonify(success='false', error_message='only HTTP DELETE/POST method allowed.'), 405
