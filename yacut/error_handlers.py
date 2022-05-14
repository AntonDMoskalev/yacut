from flask import jsonify, render_template

from . import app, db
from .views import get_unique_short_id
from .models import URL_map
import re


class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


def request_verification(data):
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса', 400)
    if not data.get('url'):
        raise InvalidAPIUsage('"url" является обязательным полем!', 400)
    custom_id = data.get('custom_id', get_unique_short_id(data['url']))
    if not custom_id:
        custom_id = get_unique_short_id(data['url'])
    if re.search('[А-Яа-я !@%#.&*+$_{+-]', custom_id) or len(custom_id) >= 16:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', 400)
    if URL_map.query.filter_by(short=custom_id).first():
        raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.', 400)
    return custom_id
