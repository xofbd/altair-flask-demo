from flask import Flask, render_template, request

from database import query_db
from plot import plot_wells

app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/plot', methods=['POST'])
def plot():
    depth_min = request.form['depth_min']
    grad_min = request.form['grad_min']

    data = query_db(depth_min, grad_min)
    chart_json = plot_wells(data)

    return render_template('plot.html', chart=chart_json)


if __name__ == '__main__':
    app.run()
