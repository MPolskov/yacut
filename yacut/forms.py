from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Добавьте ссылку',
        validators=[Length(1, 256),
                    DataRequired(message='Обязательное поле')]
    )
    custom_id = URLField(
        'Добавьте короткую ссылку (Опционально)',
        validators=[Length(1, 17), Optional()]
    )
    submit = SubmitField('Получить короткую ссылку')