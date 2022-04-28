from . import app, db
from forms import URL_mapForm
from flask import flash
from models import URL_map



@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URL_mapForm
    if form.validate_on_submit():
        short = form.short.data
