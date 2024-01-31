import random
from string import ascii_lowercase, ascii_uppercase, digits

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id():
    simbols = ascii_uppercase + ascii_lowercase + digits
    short_url_list = URLMap.query.all()
    while True:
        short = ''.join(random.choice(simbols, k=6))
        if short_url_list.filter_by(custom_id=short).first() is None:
            return short


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if URLMap.query.filter_by(custom_id=custom_id).first():
            flash('Такой url уже есть!')
            return render_template('index_view.html', form=form)
        if custom_id is None:
            custom_id = get_unique_short_id()
        url_map = URLMap(
            original=form.original_link.data,
            short=form.custom_id.data
        )
        db.session.add(url_map)
        db.session.commit()
        return redirect(url_for('opinion_view', id=opinion.id)) # TODO
    return render_template('index_view.html', form=form)


@app.route('/<string:link>')
def opinion_view(link):
    original_link = URLMap.query.filter_by(short=link).original_link
    return redirect(original_link)