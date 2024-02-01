import random

from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .constants import (
    VALID_VALUE,
    SHORT_LINK_EXIST
)


def get_unique_short_id():
    # short_url_list = URLMap.query.all()
    while True:
        short = ''.join(random.choices(VALID_VALUE, k=6))
        if URLMap.query.filter_by(short=short).first() is None:
            return short


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if URLMap.query.filter_by(short=custom_id).first():
            flash(SHORT_LINK_EXIST)
            return render_template('index_view.html', form=form)
        if not custom_id:
            custom_id = get_unique_short_id()
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
    obj = URLMap.query.filter_by(short=link).first()
    if obj is not None:
        return redirect(obj.original)
    abort(404)