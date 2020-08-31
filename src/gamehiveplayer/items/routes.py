from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from gamehiveplayer.models import Item, db

items = Blueprint('items', __name__)

@items.route('/item', methods=['GET', 'POST'])
def list_or_create_item():
    """ GET method:
            list items
            return json
                eg.
                {
                    'success': 'true',
                    'items': [
                        ...
                    ]
                }
        POST method:
            create new item
            return json
                eg.
                {
                    'success': 'true'
                }
    """
    if request.method == 'GET':
        return jsonify(success='true', items=[g.as_dict() for g in Item.query.all()]), 200
    elif request.method == 'POST':
        req_data = request.get_json()
        if not req_data:
            return jsonify(success='false', error_message='mimetype does not indicate JSON'), 404
        item = Item(name=req_data.get('name'), skill_point=req_data.get('skill_point'))
        db.session.add(item)
        try:
            db.session.commit()
        except IntegrityError as e:
            return jsonify(success='false', error_message=repr(e)), 400
        else:
            return jsonify(success='true'), 201
    else:
        return jsonify(success='false', error_message='only HTTP POST method allowed.'), 405

@items.route('/item/<name>', methods=['GET', 'POST', 'PUT'])
def update_item(name):
    """ GET method:
            show item
            return json
                eg.
                {
                    'success': 'true',
                    'item': {
                        'name': 'testitem02',
                        'skill_point': 20
                    }
                }
        POST or PUT method:
            update existing item
            return json
                eg.
                {
                    'success': 'true'
                }
    """
    if request.method == 'GET':
        i = Item.query.filter_by(name=name).first()
        if i is None:
            return jsonify(success='false', error_message='Not found'), 404
        else:
            return jsonify(success='true', item=i.as_dict()), 200
    elif request.method in ['POST', 'PUT']:
        i = Item.query.filter_by(name=name).first()
        if i is None:
            return jsonify(success='false', error_message='Not found'), 404
        else:
            req_data = request.get_json()
            i.name = req_data.get('name')
            i.skill_point = req_data.get('skill_point')
            try:
                db.session.commit()
            except IntegrityError as e:
                return jsonify(success='false', error_message=repr(e)), 400
            else:
                return jsonify(success='true'), 200
    else:
        return jsonify(success='false', error_message='only HTTP GET/POST/PUT method allowed.'), 405

@items.route('/item/<name>/delete', methods=['DELETE', 'POST'])
def delete_item(name):
    """ DELETE or POST method:
            delete a item
            return json
                eg.
                {
                    'success': 'true'
                }
    """
    if request.method in ['DELETE', 'POST']:
        i = Item.query.filter_by(name=name).first()
        if i is None:
            return jsonify(success='false', error_message='Not found'), 404
        else:
            db.session.delete(i)
            try:
                db.session.commit()
            except IntegrityError as e:
                return jsonify(success='false', error_message=repr(e)), 400
            else:
                return jsonify(success='true'), 200
    else:
        return jsonify(success='false', error_message='only HTTP DELETE/POST method allowed.'), 405
