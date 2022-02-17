from flask_wtf import FlaskForm
from wtforms import DecimalField
from wtforms.validators import DataRequired, NumberRange


class PlotForm(FlaskForm):
    depth_min = DecimalField(
        "Minimum Depth (m)",
        validators=[DataRequired(), NumberRange(min=0)]
    )
    grad_min = DecimalField(
        "Minimum Gradient (°C/m)",
        validators=[DataRequired(), NumberRange(min=0)]
    )
