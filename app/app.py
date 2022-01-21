import os

from flask import Flask, render_template, redirect, request, url_for

from app.database import query_db
from app.forms import PlotForm
from app.plot import plot_wells

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)


@app.route('/', methods=['GET', 'POST'])
def root():
    form = PlotForm()

    if form.validate_on_submit():
        return redirect(url_for('plot'), code=307)

    return render_template('index.html', form=form)


@app.route('/plot', methods=['POST'])
def plot():
    form = PlotForm(request.form)
    data = query_db(form.depth_min.data, form.grad_min.data)
    chart_json = plot_wells(data)

    return render_template('plot.html', chart=chart_json)
