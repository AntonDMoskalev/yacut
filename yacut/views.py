import re
from random import choice

from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import URL_mapForm
from .models import URL_map
from settings import URL


def get_unique_short_id(url):
    """
    Generates a short link from a long URL.
    Only Latin letters and numbers with a limit of 6 characters.
    """
    regex = re.sub('[^A-Za-z0-9]', '', url)
    short = ''.join([choice(regex) for itr in range(6)])
    return short


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """
    Function for the form on the main page.
    Checks whether the user has entered his own version of the short link,
    if there are no matches in the database,
    accepts the user's version
    (limit of 16 characters, only Latin letters and numbers).
    In case of an empty field, generates a random short link from a long address.
    """
    form = URL_mapForm()
    if form.validate_on_submit():
        short_name = form.custom_id.data
        if short_name:
            if URL_map.query.filter_by(short=short_name).first():
                flash(f'Имя {short_name} уже занято!')
                return render_template('index.html', form=form), 400
        else:
            short_name = get_unique_short_id(form.original_link.data)
        url = URL_map(original=form.original_link.data, short=short_name)
        db.session.add(url)
        db.session.commit()
        flash(f"<a href='{URL}/{short_name}' class='alert-link'>{URL}/{short_name}</a>")
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@app.route('/<string:link>', methods=['GET'])
def link_view(link):
    """
    The function returns a short link to the original address.
    If there is no link, it returns 404.
    """
    url = URL_map.query.filter_by(short=link).first()
    if not url:
        abort(404)
    return redirect(url.original)
