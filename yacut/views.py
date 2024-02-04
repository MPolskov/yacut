import random

from flask import flash, redirect, render_template

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .constants import (
    VALID_VALUE,
    SHORT_LINK_EXIST,
    SHORT_LINK_LENGTH
)


def get_unique_short_id():
    while True:
        short = ''.join(random.choices(VALID_VALUE, k=SHORT_LINK_LENGTH))
        if URLMap.query.filter_by(short=short).first() is None:
            return short


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        # Python 3.9
        if custom_id is None or custom_id == '':
            custom_id = get_unique_short_id()
        elif URLMap.query.filter_by(short=custom_id).first():
            flash(SHORT_LINK_EXIST)
            return render_template('index_view.html', form=form)
        # Python 3.10+
        # match custom_id:
        #     case '' | None:
        #         custom_id = get_unique_short_id()
        #     case id if URLMap.query.filter_by(short=id).first():
        #         flash(SHORT_LINK_EXIST)
        #         return render_template('index_view.html', form=form)
        url_map = URLMap(
            original=form.original_link.data,
            short=custom_id
        )
        db.session.add(url_map)
        db.session.commit()
        return render_template('index_view.html', short=url_map.short, form=form)
    return render_template('index_view.html', form=form)


@app.route('/<string:link>')
def redirect_view(link):
    obj = URLMap.query.filter_by(short=link).first_or_404()
    return redirect(obj.original)