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
    short_url_list = [item.short for item in URLMap.query.all()]
    count = 0
    while count < 1000:
        short = ''.join(random.choices(VALID_VALUE, k=6))
        if short not in short_url_list:
            return short
        count += 1
    abort(500)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        # Python 3.9
        if custom_id in ['', None]:
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
    obj = URLMap.query.filter_by(short=link).first()
    if obj is not None:
        return redirect(obj.original)
    abort(404)