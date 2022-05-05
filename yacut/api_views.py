from .error_handlers import InvalidAPIUsage
from . import app, db
from .models import URL_map
from flask import jsonify, request
from .views import get_unique_short_id


@app.route('/api/<int:id>/', methods=['GET'])
def get_short(short_id):
    url = URL_map.query.filter_by(short=short_id).first()
    if url is not None:
        return jsonify({'url': url.original}), 200
    raise InvalidAPIUsage("Указанный id не найден", 404)


@app.route('/api/<int:id>/', methods=['POST'])
def create_url(id):
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса', 400)
    if not data['url']:
        raise InvalidAPIUsage("\'url\' является обязательным полем!", 400)
    if not data.get('custom_id'):
        custom_id = get_unique_short_id(data['url'])
    else:
        if URL_map.query.filter_by(short=data['custom_id']).first():
            raise InvalidAPIUsage("Указано недопустимое имя для короткой ссылки", 400)
        if len(data['custom_id']) >= 16:
            raise InvalidAPIUsage('поле `short_id` содержит строку длиннее 16 символов', 400)
        custom_id = data['custom_id']
    url = URL_map(original=data['url'], short=custom_id)
    db.session.add(url)
    db.session.commit()
    return jsonify({'url': data['url'], 'custom_id': custom_id}), 201
