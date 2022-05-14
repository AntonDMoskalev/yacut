from .error_handlers import InvalidAPIUsage, request_verification
from . import app, db
from .models import URL_map
from flask import jsonify, request


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_short(short_id):
    url = URL_map.query.filter_by(short=short_id).first()
    if url is not None:
        return jsonify({'url': url.original}), 200
    raise InvalidAPIUsage("Указанный id не найден", 404)


@app.route('/api/id/', methods=['POST'])
def create_url():
    data = request.get_json()
    custom_id = request_verification(data)
    url = URL_map(original=data['url'], short=custom_id)
    db.session.add(url)
    db.session.commit()
    return jsonify({'url': data['url'], 'short_link': f'http://localhost/{custom_id}'}), 201
