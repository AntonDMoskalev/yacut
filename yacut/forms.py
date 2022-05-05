from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp


class URL_mapForm(FlaskForm):
    """
    Form for the URL map model:
    1. The original link field (Required).
    Validation for the field length (300) and checking that the link is a URL
    2. Short identifier field(Optional).
    Validation by field length(16),
    and validation via regular expression (Latin letters and numbers only).
    """
    original_link = URLField('Длинная ссылка',
                             validators=[DataRequired(message='Обязательное поле'),
                                         Length(1, 300, message='Длинная ссылка не более 300 символов'),
                                         URL(require_tld=True, message='Введите URL адрес')])
    custom_id = StringField('Ваш вариант короткой ссылки',
                            validators=[Length(1, 16, message='Короткая ссылка не более 16 символов'),
                                        Regexp(r"[A-Za-z0-9]",
                                        flags=0,
                                        message='Допускаются только буквы латинского алфавита и цифры'),
                                        Optional()])
    submit = SubmitField('Создать')
