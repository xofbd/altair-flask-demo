import os

from flask import Flask, render_template

from app.database import query_db
from app.forms import PlotForm
from app.plot import plot_wells

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)


@app.route('/', methods=['GET', 'POST'])
def root():
    form = PlotForm()

    if form.validate_on_submit():
        data = query_db(form.depth_min.data, form.grad_min.data)
        chart_json = plot_wells(data)

        return render_template('plot.html', chart=chart_json)

    return render_template('index.html', form=form)
