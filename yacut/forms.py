from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField
from wtforms.validators import DataRequired, Length, URL, Optional


class URL_mapForm(FlaskForm):
    original = URLField('Длинная ссылка',
                        validators=[
                            DataRequired(message='Обязательное поле'),
                            Length(1, 300),
                            URL(require_tld=True, message='Введите URL адрес')])
    short = URLField('Короткая строка',
                     validators=[
                         URL(require_tld=True, message='Введите URL адрес'),
                         Length(1, 16),
                         Optional()])
    submit = SubmitField('Создать')
