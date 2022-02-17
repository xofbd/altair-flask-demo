from altair.utils.data import MaxRowsError
from flask import Blueprint, flash, redirect, render_template, url_for

from app.database import get_db, query_db
from app.forms import PlotForm
from app.plot import plot_wells

bp = Blueprint("views", __name__)


@bp.route("/", methods=["GET", "POST"])
def root():
    form = PlotForm()

    if form.validate_on_submit():
        data = query_db(get_db(), form.depth_min.data, form.grad_min.data)
        try:
            chart_json = plot_wells(data)
        except MaxRowsError:
            flash(
                "Query returned too many records to visualize. "
                "Try a more restrictive query."
            )

            return redirect(url_for("views.root"))

        return render_template("plot.html", chart=chart_json)

    return render_template("index.html", form=form)
